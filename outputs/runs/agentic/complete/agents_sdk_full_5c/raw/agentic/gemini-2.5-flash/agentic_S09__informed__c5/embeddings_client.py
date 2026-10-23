import os
import google.generativeai as genai

def get_gemini_embeddings_client():
    """Provides a configured Google Gemini Embeddings client."""
    api_key = os.environ.get("GOOGLE_API_KEY")
    if not api_key:
        raise ValueError("GOOGLE_API_KEY environment variable not set.")
    genai.configure(api_key=api_key)
    return genai

