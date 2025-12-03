import os
import openai
from django.conf import settings

def get_ai_response(prompt):
    openai.api_key = os.environ.get("OPENAI_API_KEY")
    if not openai.api_key:
        return "OpenAI API key not configured."

    try:
        response = openai.Completion.create(
            model="gpt-3.5-turbo-instruct",  # Or another suitable model like "text-davinci-003"
            prompt=prompt,
            max_tokens=150,
            temperature=0.7,
        )
        return response.choices[0].text.strip()
    except Exception as e:
        return f"Error communicating with AI: {e}"
