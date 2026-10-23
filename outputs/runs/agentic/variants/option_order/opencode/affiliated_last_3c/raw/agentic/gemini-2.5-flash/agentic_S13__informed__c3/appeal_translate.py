import os
from google.cloud import translate_v2 as translate


def translate_appeal_text(text: str, target_language: str = "en") -> str:
    translate_client = translate.Client()

    # Target can be a language code or a language name.
    # For instance, 'es' for Spanish, or 'fr' for French.
    result = translate_client.translate(text, target_language=target_language)

    return result["translatedText"]
