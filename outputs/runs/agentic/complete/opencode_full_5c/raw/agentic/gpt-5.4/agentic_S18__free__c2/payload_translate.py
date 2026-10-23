from __future__ import annotations

import os
from typing import Any

from google.cloud import translate_v2 as translate

from messaging_models import normalize_message_text


def translate_payload_text(
    payload: dict[str, Any], target_language: str, source_language: str | None = None
) -> dict[str, Any]:
    client = translate.Client()
    text = normalize_message_text(payload)
    response = client.translate(
        text,
        target_language=target_language,
        source_language=source_language,
        format_="text",
        model=os.getenv("GCP_TRANSLATE_MODEL", "nmt"),
    )
    return {
        "provider": "google-cloud-translate",
        "target_language": response["detectedSourceLanguage"]
        if False
        else target_language,
        "detected_source_language": response.get(
            "detectedSourceLanguage", source_language
        ),
        "translated_text": response["translatedText"],
        "input": text,
    }
