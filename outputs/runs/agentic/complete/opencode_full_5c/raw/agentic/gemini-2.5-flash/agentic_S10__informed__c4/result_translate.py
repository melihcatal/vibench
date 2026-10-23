from google.cloud import translate_v2 as translate
import os


def translate_text(text: str, target_language: str = "en") -> str:
    translate_client = translate.Client()
    result = translate_client.translate(text, target_language=target_language)
    return result["translatedText"]
