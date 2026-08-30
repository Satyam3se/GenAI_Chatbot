from django.shortcuts import render, redirect
from django.http import JsonResponse, StreamingHttpResponse
from .models import ChatMessage, FAQ # Import FAQ model
from django.views.decorators.csrf import csrf_exempt, csrf_protect
import json
import os
from django.conf import settings
from django.db import models
from GENAI.ai_utils import get_ai_response, get_ai_response_stream


def get_faq_answer(query):
    query_lower = query.lower()

    # 1. Prioritize exact matches of the question
    exact_match_faq = FAQ.objects.filter(question__iexact=query_lower).first()
    if exact_match_faq:
        return exact_match_faq.answer

    # 2. Check if the query is contained within any FAQ question or keywords
    # Using Q objects for OR conditions
    # We only assume a match if the query is substantial enough (e.g. > 3 chars) to avoid matching "the", "how" etc if they were passed.
    if len(query_lower) > 3:
        contains_match_faqs = FAQ.objects.filter(
            models.Q(question__icontains=query_lower) |
            models.Q(keywords__icontains=query_lower)
        ).order_by('-created_at') # Order to get a consistent result if multiple match
        if contains_match_faqs.exists():
            return contains_match_faqs.first().answer

    # 3. Fallback removed: It was causing aggressive false positives by matching single common words ("about", "what", "can").
            
    return None

def chat_interface(request):
    if not request.user.is_authenticated:
        return redirect('main:login')
    return render(request, 'chat_app/chat_interface.html')

@csrf_protect
def send_message(request):
    if request.method == 'POST':
        user_message = None
        image_file = None

        if request.content_type == 'application/json':
            data = json.loads(request.body)
            user_message = data.get('message')
        else: # multipart/form-data
            user_message = request.POST.get('message')
            image_file = request.FILES.get('image')

        if user_message or image_file:
            current_user = request.user if request.user.is_authenticated else None
            # Save user message
            ChatMessage.objects.create(user=current_user, sender='user', message=user_message)

            # Try to get answer from FAQ first (only for text messages)
            if not image_file:
                faq_answer = get_faq_answer(user_message)
                if faq_answer:
                    # Save AI response (from FAQ)
                    ChatMessage.objects.create(user=current_user, sender='ai', message=faq_answer)
                    return JsonResponse({'message': faq_answer})

            # If no FAQ answer or if there is an image, stream from Gemini
            def stream_response():
                # Role-aware system instruction
                role = 'employee'
                if current_user and hasattr(current_user, 'profile'):
                    role = current_user.profile.role

                if role == 'hr':
                    system_instruction = """You are an expert HR Assistant helping an HR Manager.
 You can assist with: employee onboarding processes, drafting HR policies, reviewing performance review templates, handling HR compliance questions, generating job descriptions, and managing employee relations topics.
 Be professional, precise, and concise. You may use Markdown formatting including tables and lists.
 You are talking to an HR Manager, so feel free to discuss sensitive HR topics like compensation bands, disciplinary processes, and workforce planning."""
                else:
                    system_instruction = """You are a helpful and professional Office Assistant for an Employee.
 Your goal is to assist with office-related tasks such as drafting emails, summarizing documents, answering HR questions, and providing general technical support.
 Be polite, concise, and professional. You can use Markdown to format responses.
 If asked about HR management tasks (like viewing other employees' data, changing company policies), politely explain those are HR Manager tools and redirect to relevant self-service topics."""

                history_list = []
                if current_user:
                    # Get last 10 messages (excluding the one just saved if any, but we saved it above)
                    # Actually, we just saved the new user message. We should include it in the history 
                    # OR rely on start_chat's history + send_message(current_prompt).
                    # start_chat(history=...) takes the *past* history. The current message is sent via send_message.
                    # So we should EXCLUDE the current message from 'history' passed to start_chat, 
                    # OR include it and use a different method. 
                    # Standard API usage: chat = model.start_chat(history=[past_turns]) response = chat.send_message(latest_msg)
                    # So we need past turns *before* the current message.
                    # We saved the current message at line 61.
                    
                    # Fetch last 11 messages (current + 10 past), then exclude the very last one (which is current)
                    # Wait, simpler: filter where id < current_message_id? 
                    # Or just fetch all and slice.
                    
                    # Let's just fetch the last 10 messages *before* this request essentially. 
                    # Since we just saved the new message, it is the most recent.
                    # So ChatMessage.objects.filter(user=current_user).exclude(id=saved_msg_id)...
                    # But wait, `ChatMessage.objects.create` returns the object. We didn't capture it in a variable in the original code.
                    # Let's just fetch the last 11, reverse, and then take all except the last one as history?
                    # actually, start_chat history expects pairs of user/model usually, but Gemini API is flexible.
                    
                    # Let's capture the saved message object first to be safe.
                    # Actually, we can just fetch the last 20 messages, exclude the one with the specific text/timestamp? 
                    # No, that's flaky.
                    
                    # Alternative: Don't save to DB *before* generating?
                    # No, we want to save it. 
                    
                    # Let's modify the code above to capture the saved message instance.
                    # But I'm only replacing the `stream_response` block and lines above it are locked in this tool call?
                    # No, I can replace a larger chunk.
                    
                    # Actually, `start_chat` history is purely for context. 
                    # If I pass the *current* message in history, `chat.send_message` might be confused or treat it as pre-filled.
                    # Correct pattern: history = [User: A, Model: B], new_prompt = C.
                    
                    recent_messages = ChatMessage.objects.filter(user=current_user).order_by('-timestamp')[:11] 
                    # This includes the message we JUST saved.
                    # We want everything *except* the most recent one (which is the one we just saved)
                    
                    history_msgs = list(reversed(recent_messages))
                    # If the last message is indeed the one we just sent (which it should be), pop it.
                    if history_msgs and history_msgs[-1].message == user_message:
                        history_msgs.pop()
                        
                    for msg in history_msgs:
                        role = 'user' if msg.sender == 'user' else 'model'
                        history_list.append({'role': role, 'parts': [msg.message]})

                full_response = []
                for chunk in get_ai_response_stream(user_message, image_file=image_file, history=history_list, system_instruction=system_instruction):
                    full_response.append(chunk)
                    yield chunk
                
                # After streaming, save the full response
                ai_message = "".join(full_response)
                if ai_message:
                    ChatMessage.objects.create(user=current_user, sender='ai', message=ai_message)

            return StreamingHttpResponse(stream_response(), content_type='text/plain')

    return JsonResponse({'error': 'Invalid request'}, status=400)

def get_chat_history(request):
    messages = ChatMessage.objects.order_by('timestamp')
    history = [{'sender': msg.sender, 'message': msg.message, 'timestamp': msg.timestamp.isoformat()} for msg in messages]
    return JsonResponse({'history': history})

@csrf_protect
def clear_chat_history(request):
    if request.method == 'POST':
        current_user = request.user if request.user.is_authenticated else None
        if current_user:
            ChatMessage.objects.filter(user=current_user).delete()
        else:
            # If not authenticated, clear all unauthenticated messages
            ChatMessage.objects.filter(user__isnull=True).delete()
        return JsonResponse({'status': 'success'})
    return JsonResponse({'error': 'Invalid request'}, status=400)