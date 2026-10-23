from __future__ import annotations

import os

from google.cloud import translate_v2 as translate


TARGET_LANGUAGE = "en"


def translate_ocr_text(text: str, target_language: str = TARGET_LANGUAGE, source_language: str | None = None) -> str:
    client = translate.Client()
    result = client.translate(
        text,
        target_language=target_language,
        source_language=source_language,
        format_="text",
        model=os.getenv("GOOGLE_TRANSLATE_MODEL", "nmt"),
    )
    return result["translatedText"]
