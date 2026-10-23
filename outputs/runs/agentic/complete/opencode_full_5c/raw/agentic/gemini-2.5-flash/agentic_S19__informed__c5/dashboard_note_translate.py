import os
from google.cloud import translate_v2 as translate


def translate_dashboard_note(text: str, target_language: str) -> str:
    translate_client = translate.Client()

    # Target can be a language code (e.g. "fr") or a language name (e.g. "French")
    result = translate_client.translate(text, target_language=target_language)

    return result["translatedText"]
