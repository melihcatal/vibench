import os
from functools import lru_cache

from google import genai


def default_model() -> str:
    return os.getenv("GOOGLE_GENAI_MODEL", "gemini-2.0-flash")


@lru_cache(maxsize=1)
def client() -> genai.Client:
    return genai.Client(api_key=os.getenv("GOOGLE_API_KEY"))


def normalize_text(value):
    if value is None:
        return ""
    if isinstance(value, str):
        return value.strip()
    return str(value).strip()


def parse_json_text(text: str):
    import json

    return json.loads(text)
