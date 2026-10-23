import os
from typing import List
from google.cloud import translate_v2 as translate


def translate_transcript_segments(
    segments: List[str], target_language: str
) -> List[str]:
    translate_client = translate.Client()

    translations = []
    for text in segments:
        result = translate_client.translate(text, target_language=target_language)
        translations.append(result["translatedText"])

    return translations
