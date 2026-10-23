from google.cloud import translate_v2 as translate
import os


def record_translate(text: str, target_language: str) -> dict:
    translate_client = translate.Client()

    # Target can be a language code, such as "en" or "es".
    response = translate_client.translate(text, target_language=target_language)

    return {
        "translated_text": response["translatedText"],
        "source_language": response["detectedSourceLanguage"],
    }
