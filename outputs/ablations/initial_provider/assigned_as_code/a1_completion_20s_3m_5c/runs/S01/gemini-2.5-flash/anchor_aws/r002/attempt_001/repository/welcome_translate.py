from google.cloud import translate_v2 as translate
import os

def welcome_translate(payload, config=None):
    config = config or {}
    translate_client = translate.Client()

    text = payload["text"]
    target_language = payload["target_language"]

    result = translate_client.translate(text, target_language=target_language)

    return {
        "translated_text": result["translatedText"],
        "source_language": result["detectedSourceLanguage"]
    }
