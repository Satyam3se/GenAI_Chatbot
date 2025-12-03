from django.shortcuts import render
from django.http import JsonResponse
from .models import ChatMessage, FAQ # Import FAQ model
from django.views.decorators.csrf import csrf_exempt, csrf_protect
import json
import os
from django.conf import settings
from django.db import models
from GENAI.ai_utils import get_ai_response


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
        data = json.loads(request.body)
        user_message = data.get('message')

        if user_message:
            current_user = request.user if request.user.is_authenticated else None
            # Save user message
            ChatMessage.objects.create(user=current_user, sender='user', message=user_message)

            ai_response = None
            # Try to get answer from FAQ first
            faq_answer = get_faq_answer(user_message)
            if faq_answer:
                ai_response = faq_answer
            else:
                ai_response = get_ai_response(user_message)
                if not ai_response:
                    ai_response = "I apologize, but I cannot answer that question at the moment. Please try rephrasing your question or contact HR for further assistance."
            
            if ai_response:
                # Save AI response
                ChatMessage.objects.create(user=current_user, sender='ai', message=ai_response)
                return JsonResponse({'message': ai_response})
            else:
                return JsonResponse({'error': 'No response generated'}, status=500)

    return JsonResponse({'error': 'Invalid request'}, status=400)

def get_chat_history(request):
    messages = ChatMessage.objects.order_by('timestamp')
    history = [{'sender': msg.sender, 'message': msg.message, 'timestamp': msg.timestamp.isoformat()} for msg in messages]
    return JsonResponse({'history': history})