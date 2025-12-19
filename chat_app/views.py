from django.shortcuts import render
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
    contains_match_faqs = FAQ.objects.filter(
        models.Q(question__icontains=query_lower) |
        models.Q(keywords__icontains=query_lower)
    ).order_by('-created_at') # Order to get a consistent result if multiple match
    if contains_match_faqs.exists():
        return contains_match_faqs.first().answer

    # 3. Fallback to checking if any significant query word is in question or keywords
    query_words = [word for word in query_lower.split() if len(word) > 2]
    if query_words:
        word_query = models.Q()
        for word in query_words:
            word_query |= models.Q(question__icontains=word) | models.Q(keywords__icontains=word)
        
        word_match_faqs = FAQ.objects.filter(word_query).order_by('-created_at')
        if word_match_faqs.exists():
            return word_match_faqs.first().answer
            
    return None

def chat_interface(request):
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
                full_response = []
                for chunk in get_ai_response_stream(user_message, image_file=image_file):
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