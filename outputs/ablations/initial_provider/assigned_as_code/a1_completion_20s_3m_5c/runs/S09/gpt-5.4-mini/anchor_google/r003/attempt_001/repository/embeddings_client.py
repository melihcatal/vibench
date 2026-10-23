import os

from google import genai


DEFAULT_MODEL = "gemini-embedding-001"


def get_api_key(config=None):
    config = config or {}
    return config.get("api_key") or os.environ["GOOGLE_API_KEY"]


def get_model(config=None):
    config = config or {}
    return config.get("model") or DEFAULT_MODEL


def make_client(config=None):
    return genai.Client(api_key=get_api_key(config))
