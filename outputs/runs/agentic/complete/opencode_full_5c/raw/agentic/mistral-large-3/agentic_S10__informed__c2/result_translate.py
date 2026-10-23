import os
from typing import Optional

from google.cloud import translate_v2 as translate


def translate_text(
    text: str,
    target_language: str = "en",
    source_language: Optional[str] = None,
) -> str:
    """
    Translate generated model output using Google Cloud Translation.
    """
    client = translate.Client()

    if not client:
        raise ValueError("Google Cloud Translation client not initialized")

    result = client.translate(
        text,
        target_language=target_language,
        source_language=source_language,
    )

    return result["translatedText"]
