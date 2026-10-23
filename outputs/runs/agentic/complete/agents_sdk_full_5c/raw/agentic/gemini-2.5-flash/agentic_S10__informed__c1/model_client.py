import os
import google.generativeai as genai

def get_gemini_model(model_name: str):
    """
    Configures and returns a Google Gemini generative model client.
    Requires GOOGLE_API_KEY environment variable to be set.
    """
    api_key = os.getenv("GOOGLE_API_KEY")
    if not api_key:
        raise ValueError("GOOGLE_API_KEY environment variable not set.")
    genai.configure(api_key=api_key)
    return genai.GenerativeModel(model_name)

def get_gemini_embedding_model(model_name: str = "models/embedding-001"):
    """
    Configures and returns a Google Gemini embedding model client.
    Requires GOOGLE_API_KEY environment variable to be set.
    """
    api_key = os.getenv("GOOGLE_API_KEY")
    if not api_key:
        raise ValueError("GOOGLE_API_KEY environment variable not set.")
    genai.configure(api_key=api_key)
    return genai.get_embedding_model(model_name)

