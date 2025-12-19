import os
import google.generativeai as genai
from django.conf import settings
from PIL import Image

import time

def get_ai_response(prompt, image_file=None):
    api_key = settings.GOOGLE_API_KEY
    if not api_key:
        return "Google API key not configured."

    genai.configure(api_key=api_key)

    model = genai.GenerativeModel('gemini-flash-latest')

    # Simple retry mechanism for 429 errors
    max_retries = 3
    for attempt in range(max_retries):
        try:
            if image_file:
                image = Image.open(image_file)
                response = model.generate_content([prompt, image])
            else:
                response = model.generate_content(prompt)
            return response.text.strip()
        except Exception as e:
            if "429" in str(e) and attempt < max_retries - 1:
                time.sleep(2 ** attempt) # Exponential backoff: 1s, 2s, 4s
                continue
            return f"Error communicating with AI: {e}"

def get_ai_response_stream(prompt, image_file=None):
    api_key = settings.GOOGLE_API_KEY
    if not api_key:
        yield "Google API key not configured."
        return

    genai.configure(api_key=api_key)

    model = genai.GenerativeModel('gemini-flash-latest')

    # Streaming doesn't handle retries as easily mid-stream, but we can try for the initial connection
    try:
        if image_file:
            image = Image.open(image_file)
            responses = model.generate_content([prompt, image], stream=True)
        else:
            responses = model.generate_content(prompt, stream=True)
        
        for response in responses:
            yield response.text
    except Exception as e:
        yield f"Error communicating with AI: {e}"
