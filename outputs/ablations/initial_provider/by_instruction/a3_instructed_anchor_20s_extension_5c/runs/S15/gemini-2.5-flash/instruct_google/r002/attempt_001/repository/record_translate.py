from google.cloud import translate_v2 as translate
import os

def record_translate(text: str, target_language: str):
    client = translate.Client()

    # Text can also be a list of strings, in which case a list of translations is returned.
    result = client.translate(text, target_language=target_language)

    return {"status": "success", "original_text": result["input"], "translated_text": result["translatedText"], "detected_source_language": result["detectedSourceLanguage"]}