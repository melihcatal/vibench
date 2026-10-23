import os

from google import genai


DEFAULT_MODEL = "gemini-2.5-flash"


def get_api_key(config=None):
    config = config or {}
    return config.get("api_key") or os.environ["GOOGLE_API_KEY"]


def get_model(config=None, default=DEFAULT_MODEL):
    config = config or {}
    return config.get("model") or default


def create_client(config=None):
    return genai.Client(api_key=get_api_key(config))


def build_prompt(*parts):
    return "\n\n".join(part for part in parts if part)
