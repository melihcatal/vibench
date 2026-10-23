import os
from google.cloud import translate_v2 as translate
from typing import Optional


def translate_text(
    text: str, target_language: str = "es", source_language: Optional[str] = None
) -> str:
    """
    Translate generated model output using Google Cloud Translation.
    """
    # Google Cloud Translation uses GOOGLE_APPLICATION_CREDENTIALS environment variable
    # for authentication via service account JSON file

    client = translate.Client()

    result = client.translate(
        text, target_language=target_language, source_language=source_language
    )

    return result["translatedText"]
