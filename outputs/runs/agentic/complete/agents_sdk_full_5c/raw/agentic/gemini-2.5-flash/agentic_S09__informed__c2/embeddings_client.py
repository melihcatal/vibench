import os
import google.generativeai as genai

def get_gemini_client():
    """
    Initializes and returns a Google Gemini client for embeddings.
    Assumes GOOGLE_API_KEY is set in environment variables.
    """
    api_key = os.getenv("GOOGLE_API_KEY")
    if not api_key:
        raise ValueError("GOOGLE_API_KEY environment variable not set.")
    genai.configure(api_key=api_key)
    return genai
