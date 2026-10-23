import os
import google.generativeai as genai


def get_model_client(model_name="gemini-1.5-flash"):
    """
    Returns a configured GenerativeModel client.
    """
    api_key = os.getenv("GOOGLE_API_KEY")
    if not api_key:
        raise ValueError("GOOGLE_API_KEY environment variable not set.")

    genai.configure(api_key=api_key)
    model = genai.GenerativeModel(model_name)
    return model
