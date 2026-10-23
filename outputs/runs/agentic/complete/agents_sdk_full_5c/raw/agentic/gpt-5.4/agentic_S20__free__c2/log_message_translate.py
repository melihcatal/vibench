from __future__ import annotations

import os

from google.cloud import translate_v2 as translate


def log_message_translate(text: str, target_language: str) -> dict[str, str]:
    client = translate.Client()
    response = client.translate(
        text,
        target_language=target_language,
        format_="text",
        model="nmt",
    )
    return {
        "provider": "Google Cloud Translation",
        "target_language": target_language,
        "translated_text": response["translatedText"],
        "detected_source_language": response.get("detectedSourceLanguage", ""),
    }
