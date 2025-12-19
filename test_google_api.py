
import os
import django
import sys
from django.conf import settings

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'GENAI.settings')
django.setup()

from GENAI.ai_utils import get_ai_response

def test_api():
    with open('verification_result.txt', 'w') as f:
        f.write(f"API Key configured: {'Yes' if settings.GOOGLE_API_KEY else 'No'}\n")
        if not settings.GOOGLE_API_KEY:
            f.write("Error: API Key is missing!\n")
            return

        f.write("Sending request to Gemini (gemini-2.0-flash)...\n")
        try:
            response = get_ai_response("Hello, are you working?")
            if "Error communicating with AI" in response:
                f.write(f"FAILED: {response}\n")
            else:
                f.write(f"Response: {response}\n")
                f.write("SUCCESS: Google API is working!\n")
        except Exception as e:
            f.write(f"FAILED EXCEPTION: {e}\n")

if __name__ == "__main__":
    test_api()
