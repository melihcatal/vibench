import os
from google import genai

def get_genai_client(config=None):
    config = config or {}
    api_key = config.get("api_key") or os.environ.get("GOOGLE_API_KEY")
    if not api_key:
        raise ValueError("GOOGLE_API_KEY not found in config or environment variables.")
    return genai.Client(api_key=api_key)

def get_default_model_id():
    return "gemini-2.5-flash"
