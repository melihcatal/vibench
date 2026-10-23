from __future__ import annotations

from typing import Optional

from google.cloud import translate_v2 as translate


def translate_runbook_notes(text: str, target_language: str, source_language: Optional[str] = None) -> dict:
    client = translate.Client()
    response = client.translate(
        text,
        target_language=target_language,
        source_language=source_language,
        format_="text",
    )
    return {
        "translated_text": response["translatedText"],
        "detected_source_language": response.get("detectedSourceLanguage"),
        "provider": "google-cloud-translate-v2",
    }
