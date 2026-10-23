import os
from google.cloud import translate_v2 as translate
from typing import List, Dict, Any, Optional


def runbook_translate(
    text: str, target_language: str = "en", source_language: Optional[str] = None
) -> Dict[str, Any]:
    """Translate secret-rotation runbook notes using Google Cloud Translation."""
    credentials_path = os.environ.get("GOOGLE_APPLICATION_CREDENTIALS")
    if not credentials_path:
        raise ValueError(
            "GOOGLE_APPLICATION_CREDENTIALS environment variable must be set"
        )

    client = translate.Client()

    try:
        if source_language:
            result = client.translate(
                text,
                target_language=target_language,
                source_language=source_language,
                format_="text",
            )
        else:
            result = client.translate(
                text, target_language=target_language, format_="text"
            )

        translation = {
            "original_text": text,
            "translated_text": result["translatedText"],
            "target_language": target_language,
            "detected_source_language": result.get("detectedSourceLanguage"),
            "model": "nmt",  # Google's Neural Machine Translation
            "provider": "google",
        }

        return translation

    except Exception as e:
        raise Exception(f"Translation failed: {e}")
