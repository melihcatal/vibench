import os
from google.cloud import translate_v2 as translate

def ocr_translate(text: str, target_language: str = "en") -> dict:
    client = translate.Client()
    result = client.translate(text, target_language=target_language)
    return {
        "translated_text": result["translatedText"],
        "detected_source_language": result["detectedSourceLanguage"]
    }
