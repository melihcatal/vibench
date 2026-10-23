import os
import google.generativeai as genai


def get_gemini_client():
    """Configures and returns a Google Gemini client."""
    api_key = os.environ.get("GOOGLE_API_KEY")
    if not api_key:
        raise ValueError("GOOGLE_API_KEY environment variable not set.")
    genai.configure(api_key=api_key)
    return genai


def get_generative_model(model_name: str = "gemini-pro"):
    """Returns a GenerativeModel instance."""
    client = get_gemini_client()
    return client.GenerativeModel(model_name)
