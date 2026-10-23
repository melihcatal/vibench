import os
import google.generativeai as genai

def get_gemini_embedding_model(api_key: str = None):
    """Initializes and returns the Gemini embedding model."""
    if api_key is None:
        api_key = os.environ.get("GOOGLE_API_KEY")
        if not api_key:
            raise ValueError("GOOGLE_API_KEY environment variable not set and no API key provided.")
    genai.configure(api_key=api_key)
    return genai.get_model("models/embedding-001")

def get_generative_client(api_key: str = None):
    """Initializes and returns a generative AI client."""
    if api_key is None:
        api_key = os.environ.get("GOOGLE_API_KEY")
        if not api_key:
            raise ValueError("GOOGLE_API_KEY environment variable not set and no API key provided.")
    return genai.Client(api_key=api_key)
