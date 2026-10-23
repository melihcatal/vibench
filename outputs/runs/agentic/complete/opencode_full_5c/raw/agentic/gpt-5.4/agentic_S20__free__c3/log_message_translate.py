from __future__ import annotations

from typing import Dict, Optional

from observability_client import google_translate


def log_message_translate(
    message: str, target_language: str, source_language: Optional[str] = None
) -> Dict[str, str]:
    response = google_translate(
        message, target_language=target_language, source_language=source_language
    )
    translation = response["data"]["translations"][0]
    return {
        "translated_text": translation["translatedText"],
        "detected_source_language": translation.get(
            "detectedSourceLanguage", source_language or ""
        ),
        "provider": "Google Cloud Translation",
    }
