from google.cloud import translate_v2 as translate
import os


def script_translate(text: str, target_language: str) -> str:
    client = translate.Client()
    result = client.translate(text, target_language=target_language)
    return result["translatedText"]
