import os
from google.cloud import translate_v2 as translate
from typing import Dict, Any

def translate_text(payload: Dict[str, Any], config: Dict[str, Any] = None) -> Dict[str, Any]:
    config = config or {}
    target_language = payload.get("target_language", "en")
    text_to_translate = payload.get("text", "")

    # Google Cloud Translation V2 client
    # Ensure GOOGLE_APPLICATION_CREDENTIALS or default credentials are set up
    translate_client = translate.Client()

    if isinstance(text_to_translate, bytes):
        text_to_translate = text_to_translate.decode("utf-8")

    # Detect the source language and translate
    result = translate_client.translate(text_to_translate, target_language=target_language)

    translated_text = result["translatedText"]
    detected_source_language = result["detectedSourceLanguage"]

    return {
        "translated_text": translated_text,
        "source_language": detected_source_language,
        "target_language": target_language,
    }
