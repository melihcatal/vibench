from typing import Dict, Any
import os
from google.cloud import translate_v2 as translate


def invoice_note_translate(text: str, target_language: str = "en") -> str:
    """
    Translates extracted invoice notes or descriptions using Google Cloud Translation.
    """
    if not os.getenv("GOOGLE_APPLICATION_CREDENTIALS"):
        raise ValueError(
            "Google Cloud credentials must be set in environment variables."
        )

    client = translate.Client()

    result = client.translate(text, target_language=target_language)
    return result["translatedText"]
