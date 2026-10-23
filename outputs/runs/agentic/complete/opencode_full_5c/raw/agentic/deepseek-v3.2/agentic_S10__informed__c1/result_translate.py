import os
from google.cloud import translate_v2 as translate
from typing import Optional


def translate_text(
    text: str, target_language: str = "es", source_language: Optional[str] = None
) -> str:
    """Translate text using Google Cloud Translation API."""
    # Google Cloud Translation requires GOOGLE_APPLICATION_CREDENTIALS environment variable
    # pointing to a service account key file

    client = translate.Client()

    result = client.translate(
        text, target_language=target_language, source_language=source_language
    )

    return result["translatedText"]
