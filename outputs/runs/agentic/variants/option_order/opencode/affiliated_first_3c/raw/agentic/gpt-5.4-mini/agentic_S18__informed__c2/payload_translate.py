import os

from deep_translator import GoogleTranslator


def translate_payload_text(text: str, target_language: str) -> str:
    return GoogleTranslator(source="auto", target=target_language).translate(text)
