import google.generativeai as genai
import os

def get_gemini_client():
    """
    Provides local configuration and client helper utilities for Google Gemini API.
    """
    api_key = os.environ.get("GOOGLE_API_KEY")
    if not api_key:
        raise ValueError("GOOGLE_API_KEY environment variable not set.")
    genai.configure(api_key=api_key)
    return genai

def get_gemini_model(model_name: str = "gemini-pro"):
    """
    Returns a configured Gemini GenerativeModel instance.
    """
    genai_client = get_gemini_client()
    return genai_client.GenerativeModel(model_name)
