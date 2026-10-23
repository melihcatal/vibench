import os
from google.cloud import translate_v2 as translate


def translate_transcript_segment(text: str, target_language: str) -> str:
    translate_client = translate.Client()

    # Target can be a language code or a language name
    result = translate_client.translate(text, target_language=target_language)

    return result["translatedText"]
