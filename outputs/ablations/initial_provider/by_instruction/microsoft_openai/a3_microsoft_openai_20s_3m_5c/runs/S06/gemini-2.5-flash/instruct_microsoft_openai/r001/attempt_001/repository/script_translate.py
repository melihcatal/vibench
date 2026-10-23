from google.cloud import translate_v2 as translate
import os

def script_translate(text: str, target_language: str = "es") -> str:
    """
    Translates narration scripts using Google Cloud Translation.
    """
    translate_client = translate.Client()

    result = translate_client.translate(
        text,
        target_language=target_language
    )

    return result["translatedText"]
