from __future__ import annotations

from google.cloud import translate_v2 as translate


def translate_script(text: str, target_language: str, source_language: str | None = None) -> str:
    client = translate.Client()
    result = client.translate(
        text,
        target_language=target_language,
        source_language=source_language,
        format_="text",
    )
    return result["translatedText"]
