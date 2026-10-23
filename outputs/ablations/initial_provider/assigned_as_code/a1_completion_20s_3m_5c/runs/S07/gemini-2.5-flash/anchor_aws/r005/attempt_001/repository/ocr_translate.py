from google.cloud import translate_v2 as translate
import os

def ocr_translate(text: str, target_language: str, config=None):
    config = config or {}
    translate_client = translate.Client()

    result = translate_client.translate(text, target_language=target_language)

    return {"translated_text": result["translatedText"], "detected_source_language": result["detectedSourceLanguage"]}
