import os
from typing import Dict, Any
from google.cloud import translate_v2 as translate

def translate_output(text: str, target_language: str) -> Dict[str, Any]:
    """
    Translates Cohere model output to another locale using Google Cloud Translation API.
    Returns translated text and detected source language.
    """
    client = translate.Client()
    result = client.translate(text, target_language=target_language)

    return {
        "translated_text": result["translatedText"],
        "detected_source_language": result["detectedSourceLanguage"],
        "target_language": target_language,
    }