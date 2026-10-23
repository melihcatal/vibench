from __future__ import annotations

from typing import Optional

from google.cloud import translate_v2 as translate


GOOGLE_TRANSLATE_MODEL = "nmt"


def translate_payload_text(
    text: str,
    *,
    target_language: str,
    source_language: Optional[str] = None,
) -> str:
    client = translate.Client()
    response = client.translate(
        text,
        target_language=target_language,
        source_language=source_language,
        model=GOOGLE_TRANSLATE_MODEL,
        format_="text",
    )
    return str(response["translatedText"])
