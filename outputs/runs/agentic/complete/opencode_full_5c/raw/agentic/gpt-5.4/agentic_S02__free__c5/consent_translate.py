from __future__ import annotations

import os

from google.cloud import translate_v2 as translate


def consent_translate(
    text: str, target_language: str, source_language: str | None = None
) -> dict[str, str]:
    client = translate.Client()
    response = client.translate(
        text,
        target_language=target_language,
        source_language=source_language,
        format_="text",
    )
    return {
        "provider": "google_cloud_translate",
        "project": os.getenv("GOOGLE_CLOUD_PROJECT", ""),
        "translated_text": response["translatedText"],
        "detected_source_language": response.get(
            "detectedSourceLanguage", source_language or ""
        ),
        "target_language": target_language,
    }
