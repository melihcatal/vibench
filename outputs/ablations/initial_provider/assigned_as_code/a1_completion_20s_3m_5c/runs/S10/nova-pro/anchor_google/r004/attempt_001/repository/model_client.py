import os


def get_api_key():
    return os.environ.get("GOOGLE_API_KEY")


def get_client():
    from google import genai
    return genai.Client(api_key=get_api_key())