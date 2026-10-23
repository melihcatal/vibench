from typing import Optional

from google.cloud import translate_v2 as translate


def alt_text_translate(
    text: str, target_language: str, source_language: Optional[str] = None
) -> str:
    client = translate.Client()
    result = client.translate(
        text, target_language=target_language, source_language=source_language
    )
    return result["translatedText"]
