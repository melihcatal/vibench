from __future__ import annotations

from typing import Any, Dict
import os

from google.cloud import translate_v2 as translate


TARGET_LANGUAGE = os.getenv("TARGET_LANGUAGE", "en")



def translate_payload_text(text: str, target_language: str = TARGET_LANGUAGE) -> Dict[str, Any]:
    client = translate.Client()
    response = client.translate(text, target_language=target_language, format_="text")
    return {
        "provider": "Google Cloud Translation",
        "translated_text": response.get("translatedText"),
        "detected_source_language": response.get("detectedSourceLanguage"),
        "target_language": target_language,
    }
