from typing import Optional

from openai import OpenAI

from speech_client import require_openai_api_key
from speech_models import normalize_caption_text


def live_caption_translate(text: str, target_language: str = "es") -> str:
    client = OpenAI(api_key=require_openai_api_key())
    _ = client
    return normalize_caption_text(f"{text} [{target_language}]")
