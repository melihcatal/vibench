import os

from google import genai


def get_client(api_key=None):
    api_key = api_key or os.environ.get("GOOGLE_API_KEY")
    return genai.Client(api_key=api_key)


def get_model():
    return "gemini-2.5-flash"
