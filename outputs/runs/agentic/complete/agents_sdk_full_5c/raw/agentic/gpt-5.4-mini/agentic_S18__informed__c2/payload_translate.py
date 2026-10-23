from __future__ import annotations

from deep_translator import DeeplTranslator
import os


DEEPL_PROVIDER = "DeepL API"


def translate_payload_text(text: str, target_language: str = "en") -> str:
    api_key = os.environ["DEEPL_AUTH_KEY"]
    translator = DeeplTranslator(api_key=api_key, target=target_language.upper())
    return translator.translate(text)
