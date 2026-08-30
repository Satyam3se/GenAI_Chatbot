import os
from openai import OpenAI
from django.conf import settings
from PIL import Image
import base64
import time

def get_ai_response(prompt, image_file=None):
    api_key = settings.GROQ_API_KEY
    if not api_key:
        return "Groq API key not configured."

    client = OpenAI(
        api_key=api_key,
        base_url="https://api.groq.com/openai/v1"
    )
    
    max_retries = 3
    for attempt in range(max_retries):
        try:
            messages = [{"role": "user", "content": []}]
            
            if image_file:
                with open(image_file, "rb") as image_f:
                    base64_image = base64.b64encode(image_f.read()).decode('utf-8')
                
                messages[0]["content"].append({"type": "text", "text": prompt})
                messages[0]["content"].append({
                    "type": "image_url",
                    "image_url": {"url": f"data:image/jpeg;base64,{base64_image}"}
                })
                model = "openai/gpt-oss-120b" # Groq vision model
            else:
                messages[0]["content"] = prompt
                model = "openai/gpt-oss-120b" # Fast Groq text model
                
            response = client.chat.completions.create(
                model=model,
                messages=messages
            )
            return response.choices[0].message.content.strip()
        except Exception as e:
            if "429" in str(e) and attempt < max_retries - 1:
                time.sleep(2 ** attempt)
                continue
            return f"Error communicating with AI: {e}"

def get_ai_response_stream(prompt, image_file=None, history=None, system_instruction=None):
    api_key = settings.GROQ_API_KEY
    if not api_key:
        yield "Groq API key not configured."
        return

    client = OpenAI(
        api_key=api_key,
        base_url="https://api.groq.com/openai/v1"
    )
    
    try:
        messages = []
        if system_instruction:
            messages.append({"role": "system", "content": system_instruction})
            
        if history:
            for item in history:
                role = "assistant" if item['role'] == "model" else item['role']
                content = item['parts'][0] if 'parts' in item else item.get('content', '')
                messages.append({"role": role, "content": content})
                
        if image_file:
            model = "openai/gpt-oss-120b" # Groq vision model
            with open(image_file, "rb") as image_f:
                base64_image = base64.b64encode(image_f.read()).decode('utf-8')
            
            messages.append({
                "role": "user",
                "content": [
                    {"type": "text", "text": prompt},
                    {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{base64_image}"}}
                ]
            })
        else:
            model = "openai/gpt-oss-120b" # Fast Groq text model
            messages.append({"role": "user", "content": prompt})
            
        responses = client.chat.completions.create(
            model=model,
            messages=messages,
            stream=True
        )
        
        for response in responses:
            if response.choices and len(response.choices) > 0 and response.choices[0].delta.content is not None:
                yield response.choices[0].delta.content
    except Exception as e:
        yield f"Error communicating with AI: {e}"
