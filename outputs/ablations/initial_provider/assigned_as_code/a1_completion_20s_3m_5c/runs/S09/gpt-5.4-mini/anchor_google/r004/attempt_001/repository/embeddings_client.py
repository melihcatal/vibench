import os

from google import genai


def get_api_key(config=None):
    config = config or {}
    return config.get("api_key") or os.environ["GOOGLE_API_KEY"]


def get_client(config=None):
    return genai.Client(api_key=get_api_key(config))


def get_model(config=None):
    config = config or {}
    return config.get("model") or "gemini-embedding-001"
