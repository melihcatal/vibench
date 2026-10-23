import os

from deep_translator import DeeplTranslator


def translate_payload(text: str, target_language: str = "EN-US") -> str:
    auth_key = os.getenv("DEEPL_AUTH_KEY")
    if not auth_key:
        raise RuntimeError("DEEPL_AUTH_KEY is required")
    translator = DeeplTranslator(
        api_key=auth_key, source="auto", target=target_language
    )
    return translator.translate(text)
