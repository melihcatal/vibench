from google.cloud import translate_v2 as translate
import os
from typing import Dict, Any


def translate_output(text: str, target_language: str = "es") -> Dict[str, Any]:
    """Translate text using Google Cloud Translation."""
    client = translate.Client()
    
    result = client.translate(text, target_language=target_language)
    
    return {
        "translated_text": result["translatedText"],
        "detected_source_language": result["detectedSourceLanguage"],
        "input_text": text
    }