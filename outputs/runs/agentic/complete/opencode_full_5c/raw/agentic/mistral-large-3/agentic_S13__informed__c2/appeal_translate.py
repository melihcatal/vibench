from typing import Dict, Optional
import os
from google.cloud import translate_v2 as translate


def appeal_translate(
    text: str,
    target_language: str = "en",
    source_language: Optional[str] = None,
) -> Dict[str, str]:
    """
    Translate appeal text for review using Google Cloud Translation.
    """
    if not os.getenv("GOOGLE_APPLICATION_CREDENTIALS"):
        raise ValueError("Google Cloud credentials not configured")

    client = translate.Client()

    result = client.translate(
        text,
        target_language=target_language,
        source_language=source_language,
    )

    return {
        "translated_text": result["translatedText"],
        "detected_source_language": result["detectedSourceLanguage"],
        "target_language": target_language,
    }
