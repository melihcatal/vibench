from typing import Optional
from google.cloud import translate_v2 as translate


def translate_output(
    text: str, target_language: str = "es", source_language: Optional[str] = None
) -> str:
    translate_client = translate.Client()
    result = translate_client.translate(
        text, target_language=target_language, source_language=source_language
    )
    return result["translatedText"]
