from __future__ import annotations

from typing import Any, Dict

from google.cloud import translate_v2 as translate


def dashboard_note_translate(text: str, target_language: str, source_language: str | None = None) -> Dict[str, Any]:
    client = translate.Client()
    response = client.translate(
        values=text,
        target_language=target_language,
        source_language=source_language,
        format_="text",
        model="nmt",
    )
    return {
        "provider": "Google Cloud Translation API",
        "translated_text": response["translatedText"],
        "detected_source_language": response.get("detectedSourceLanguage", source_language),
        "target_language": target_language,
        "model": "nmt",
    }
