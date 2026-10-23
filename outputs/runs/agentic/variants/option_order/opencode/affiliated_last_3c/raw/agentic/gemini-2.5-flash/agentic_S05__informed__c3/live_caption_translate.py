import os
from google.cloud import translate_v2 as translate


def translate_caption(text: str, target_language: str = "es") -> dict:
    # GOOGLE_APPLICATION_CREDENTIALS environment variable is expected to be set
    translate_client = translate.Client()

    result = translate_client.translate(text, target_language=target_language)

    return {
        "original_text": result["input"],
        "translated_text": result["translatedText"],
        "source_language": result["detectedSourceLanguage"],
        "target_language": target_language,
    }
