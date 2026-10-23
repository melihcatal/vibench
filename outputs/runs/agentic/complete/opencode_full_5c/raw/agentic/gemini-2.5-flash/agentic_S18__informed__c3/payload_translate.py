from google.cloud import translate_v2 as translate
import os


def translate_text(text: str, target_language: str = "en") -> dict:
    # GOOGLE_APPLICATION_CREDENTIALS environment variable should be set
    translate_client = translate.Client()

    result = translate_client.translate(text, target_language=target_language)

    return {
        "translated_text": result["translatedText"],
        "original_text": result["input"],
        "source_language": result["detectedSourceLanguage"],
    }
