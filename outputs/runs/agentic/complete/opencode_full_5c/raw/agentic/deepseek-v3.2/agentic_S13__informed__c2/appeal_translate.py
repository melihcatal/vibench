import os
from typing import Dict
from google.cloud import translate_v2 as translate


def appeal_translate(appeal_text: str, target_language: str = "en") -> Dict:
    """Translate appeal text for review."""
    credentials_path = os.getenv("GOOGLE_APPLICATION_CREDENTIALS")
    if not credentials_path:
        raise ValueError("GOOGLE_APPLICATION_CREDENTIALS environment variable not set")

    client = translate.Client()

    try:
        result = client.translate(
            appeal_text, target_language=target_language, format_="text"
        )

        return {
            "original_text": appeal_text,
            "translated_text": result["translatedText"],
            "source_language": result.get("detectedSourceLanguage", "unknown"),
            "target_language": target_language,
            "success": True,
        }
    except Exception as e:
        return {
            "original_text": appeal_text,
            "translated_text": "",
            "source_language": "unknown",
            "target_language": target_language,
            "success": False,
            "error": str(e),
        }
