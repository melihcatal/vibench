import os

from deepl import Translator


def translate_transcript(text: str, target_language: str = "EN-US") -> str:
    auth_key = os.environ.get("DEEPL_AUTH_KEY", "")
    if not auth_key:
        raise ValueError("DEEPL_AUTH_KEY is required")
    translator = Translator(auth_key)
    result = translator.translate_text(text, target_lang=target_language)
    return getattr(result, "text", str(result))
