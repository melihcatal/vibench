import os
from typing import Dict, Any, Optional
from google.cloud import translate_v2 as translate


def payload_translate(
    text: str, target_language: str = "es", source_language: Optional[str] = None
) -> Dict[str, Any]:
    """Translate customer-facing message payload text using Google Cloud Translation."""
    credentials_path = os.getenv("GOOGLE_APPLICATION_CREDENTIALS")
    if not credentials_path:
        raise ValueError("GOOGLE_APPLICATION_CREDENTIALS environment variable not set")

    try:
        client = translate.Client()

        result = client.translate(
            text,
            target_language=target_language,
            source_language=source_language,
            format_="text",
        )

        return {
            "original_text": text,
            "translated_text": result["translatedText"],
            "source_language": result.get("detectedSourceLanguage", source_language),
            "target_language": target_language,
            "provider": "Google Cloud Translation",
            "model": "nmt",  # Neural Machine Translation
            "character_count": len(text),
        }
    except Exception as e:
        return {
            "error": str(e),
            "original_text": text,
            "target_language": target_language,
            "provider": "Google Cloud Translation",
            "translated_text": None,
        }
