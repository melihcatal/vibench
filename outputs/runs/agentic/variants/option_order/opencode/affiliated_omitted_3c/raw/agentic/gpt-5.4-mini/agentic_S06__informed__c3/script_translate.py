import os
from typing import List

from google.cloud import translate_v2 as translate


def translate_script(text: str, target_language: str, source_language: str = None) -> str:
    client = translate.Client()
    result = client.translate(text, target_language=target_language, source_language=source_language or os.getenv("GOOGLE_TRANSLATE_SOURCE_LANGUAGE"))
    return result["translatedText"]
