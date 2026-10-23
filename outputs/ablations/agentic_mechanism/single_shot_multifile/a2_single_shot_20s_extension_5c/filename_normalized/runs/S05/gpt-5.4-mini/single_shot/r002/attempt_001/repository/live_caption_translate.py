import os
from typing import Optional

from openai import OpenAI

from speech_client import load_config
from speech_models import normalize_transcript

TARGET_TRANSLATION_MODEL = os.getenv("OPENAI_TRANSLATION_MODEL", "gpt-4.1-mini")


def translate_live_caption(text: str, target_language: str) -> str:
    client = OpenAI(api_key=load_config().api_key, base_url=load_config().base_url)
    prompt = f"Translate the following caption into {target_language}. Return only the translation.\n\n{text}"
    response = client.responses.create(model=TARGET_TRANSLATION_MODEL, input=prompt)
    translated = getattr(response, "output_text", "")
    return normalize_transcript(translated)
