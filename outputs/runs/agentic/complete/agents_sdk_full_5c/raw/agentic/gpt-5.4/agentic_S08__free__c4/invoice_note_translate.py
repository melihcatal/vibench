from __future__ import annotations

import os
from typing import Optional

from google.cloud import translate_v2 as translate


GOOGLE_TARGET_LANGUAGE = os.getenv("GOOGLE_TARGET_LANGUAGE", "en")


def invoice_note_translate(text: str, target_language: Optional[str] = None) -> str:
    client = translate.Client()
    result = client.translate(
        text,
        target_language=target_language or GOOGLE_TARGET_LANGUAGE,
        format_="text",
    )
    return result["translatedText"]
