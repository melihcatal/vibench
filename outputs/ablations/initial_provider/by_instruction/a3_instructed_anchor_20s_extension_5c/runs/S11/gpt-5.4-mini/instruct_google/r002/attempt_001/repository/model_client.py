import os
from typing import Optional

from google import genai


def get_google_api_key() -> Optional[str]:
    return os.environ.get("GOOGLE_API_KEY") or os.environ.get("GEMINI_API_KEY")


def get_google_client() -> genai.Client:
    api_key = get_google_api_key()
    if api_key:
        return genai.Client(api_key=api_key)
    return genai.Client()


def get_default_model() -> str:
    return os.environ.get("GOOGLE_GENAI_MODEL", "gemini-2.0-flash")


def get_default_locale() -> str:
    return os.environ.get("PLATFORM_LOCALE", "en-US")
