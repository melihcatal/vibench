import os
from functools import lru_cache

from google import genai


def get_api_key() -> str:
    return os.environ.get("GOOGLE_API_KEY", "")


def get_model_name(default: str = "gemini-2.0-flash") -> str:
    return os.environ.get("GOOGLE_MODEL", default)


@lru_cache(maxsize=1)
def get_client() -> genai.Client:
    return genai.Client(api_key=get_api_key())


def build_text_request(system_instruction: str | None, user_text: str) -> dict:
    payload = {"model": get_model_name(), "contents": user_text}
    if system_instruction:
        payload["config"] = {"system_instruction": system_instruction}
    return payload
