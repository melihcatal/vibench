import os
from typing import Dict, Any
from google.cloud import translate_v2 as translate


def translate_appeal_text(text: str, target_language: str = "en") -> str:
    """
    Translates appeal text for review using Google Cloud Translation.
    """
    if not os.getenv("GOOGLE_APPLICATION_CREDENTIALS"):
        raise ValueError(
            "Google Cloud credentials not found. Set GOOGLE_APPLICATION_CREDENTIALS."
        )

    client = translate.Client()

    try:
        result = client.translate(text, target_language=target_language)
        return result["translatedText"]
    except Exception as e:
        raise Exception(f"Google Cloud Translation failed: {str(e)}")
