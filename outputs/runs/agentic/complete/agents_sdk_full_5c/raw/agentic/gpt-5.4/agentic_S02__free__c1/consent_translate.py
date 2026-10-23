from __future__ import annotations

import os

from google.cloud import translate_v2 as translate


_TARGET_PROJECT = os.environ.get("GOOGLE_CLOUD_PROJECT")


def translate_consent_copy(text: str, target_language: str, source_language: str | None = None) -> str:
    client = translate.Client()
    response = client.translate(
        values=text,
        target_language=target_language,
        source_language=source_language,
        format_="text",
    )
    if isinstance(response, list):
        return str(response[0]["translatedText"])
    return str(response["translatedText"])
