import google.generativeai as genai
import os

def get_gemini_model(model_name: str):
    """
    Initializes and returns a Google Gemini generative model client.
    Expects GOOGLE_API_KEY to be set in environment variables.
    """
    api_key = os.getenv("GOOGLE_API_KEY")
    if not api_key:
        raise ValueError("GOOGLE_API_KEY environment variable not set.")
    genai.configure(api_key=api_key)
    return genai.GenerativeModel(model_name)

def get_gemini_embedding_model(model_name: str = "models/embedding-001"):
    """
    Initializes and returns a Google Gemini embedding model client.
    Expects GOOGLE_API_KEY to be set in environment variables.
    """
    api_key = os.getenv("GOOGLE_API_KEY")
    if not api_key:
        raise ValueError("GOOGLE_API_KEY environment variable not set.")
    genai.configure(api_key=api_key)
    return genai.get_embedding_model(model_name)
