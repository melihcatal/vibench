import os

from google.cloud import translate_v2 as translate


TARGET_LANGUAGE = os.environ.get("ALT_TEXT_TARGET_LANGUAGE", "es")


def translate_alt_text(text: str, target_language: str = TARGET_LANGUAGE) -> str:
    client = translate.Client()
    translated = client.translate(text, target_language=target_language)
    return translated.get("translatedText", "")
