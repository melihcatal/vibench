import os
import google.generativeai as genai


def get_gemini_client():
    """
    Provides local configuration and client helper utilities for Google Gemini API.
    """
    api_key = os.environ.get("GOOGLE_API_KEY")
    if not api_key:
        raise ValueError("GOOGLE_API_KEY environment variable not set.")
    genai.configure(api_key=api_key)
    return genai
