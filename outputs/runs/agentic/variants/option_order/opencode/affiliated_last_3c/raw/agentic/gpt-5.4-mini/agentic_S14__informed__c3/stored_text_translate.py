from typing import Optional

from google.cloud import translate_v2 as translate


def translate_text(
    text: str, target_language: str, source_language: Optional[str] = None
):
    client = translate.Client()
    return client.translate(
        text, target_language=target_language, source_language=source_language
    )
