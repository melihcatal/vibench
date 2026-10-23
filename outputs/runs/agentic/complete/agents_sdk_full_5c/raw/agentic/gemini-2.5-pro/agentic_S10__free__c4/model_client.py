import os
import google.generativeai as genai

_client = None

def get_model(model_name: str):
    """Initializes and returns a generative model client."""
    global _client
    if _client is None:
        api_key = os.getenv("GOOGLE_API_KEY")
        if not api_key:
            raise ValueError("GOOGLE_API_KEY environment variable not set.")
        genai.configure(api_key=api_key)
    
    model = genai.GenerativeModel(model_name)
    return model
