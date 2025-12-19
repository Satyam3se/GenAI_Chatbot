
import os
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()
api_key = os.environ.get("GOOGLE_API_KEY")

with open('model_list_output.txt', 'w') as f:
    if not api_key:
        f.write("API Key not found in environment!\n")
    else:
        genai.configure(api_key=api_key)
        f.write("Listing available models:\n")
        try:
            for m in genai.list_models():
                f.write(f"{m.name}\n")
        except Exception as e:
            f.write(f"Error listing models: {e}\n")
