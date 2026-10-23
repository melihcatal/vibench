import os
from google.cloud import translate_v2 as translate


def translate_script(
    text: str, target_language: str, source_language: str = None
) -> str:
    client = translate.Client()

    result = client.translate(
        text, target_language=target_language, source_language=source_language
    )
    return result["translatedText"]
