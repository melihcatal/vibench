import os

from google import genai


DEFAULT_MODEL = "gemini-2.5-flash"


def get_api_key(config=None):
    config = config or {}
    return config.get("api_key") or os.environ["GOOGLE_API_KEY"]


def get_model_name(config=None, default=DEFAULT_MODEL):
    config = config or {}
    return config.get("model") or default


def client_from_config(config=None):
    return genai.Client(api_key=get_api_key(config))
