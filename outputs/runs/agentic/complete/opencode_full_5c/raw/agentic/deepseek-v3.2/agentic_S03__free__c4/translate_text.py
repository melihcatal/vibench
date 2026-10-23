import os
from google.cloud import translate_v2 as translate


def translate_text(
    text: str, target_language: str = "es", source_language: str = "en"
) -> str:
    """Translate a single text string between languages using Google Cloud Translation API."""
    client = translate.Client()

    result = client.translate(
        text, target_language=target_language, source_language=source_language
    )

    return result["translatedText"]
