import os
from typing import Optional

from google.cloud import translate_v2 as translate


def translate_extracted_text(
    text: str,
    target_language: str = "en",
    source_language: Optional[str] = None,
) -> str:
    """
    Translates text extracted from a stored document using Google Cloud Translation API.

    Args:
        text: Text to translate.
        target_language: Target language code (e.g., 'en', 'es').
        source_language: Optional source language code. If None, auto-detection is used.

    Returns:
        str: Translated text.

    Raises:
        Exception: If translation fails.
    """
    client = translate.Client(credentials=os.getenv("GOOGLE_APPLICATION_CREDENTIALS"))

    result = client.translate(
        text,
        target_language=target_language,
        source_language=source_language,
    )

    return result["translatedText"]
