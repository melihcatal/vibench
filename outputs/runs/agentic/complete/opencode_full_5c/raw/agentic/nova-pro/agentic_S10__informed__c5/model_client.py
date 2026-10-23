import os
from google.generativeai import GenerativeModel


def get_model_client():
    api_key = os.getenv("GOOGLE_API_KEY")
    if not api_key:
        raise ValueError("GOOGLE_API_KEY environment variable not set")
    model = GenerativeModel("gemini-pro")
    return model
