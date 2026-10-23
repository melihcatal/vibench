import google.generativeai as genai
import os


def get_gemini_embeddings_client():
    """Configures and returns a Gemini embeddings client."""
    api_key = os.getenv("GOOGLE_API_KEY")
    if not api_key:
        raise ValueError("GOOGLE_API_KEY environment variable not set.")
    genai.configure(api_key=api_key)
    return genai
