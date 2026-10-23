import os
from typing import Dict, Any
from google.cloud import translate_v2 as translate


def translate_invoice_note(text: str, target_language: str = "en") -> Dict[str, Any]:
    if not text:
        return {"translated_text": "", "detected_language": ""}

    client = translate.Client()
    result = client.translate(text, target_language=target_language)

    return {
        "translated_text": result["translatedText"],
        "detected_language": result["detectedSourceLanguage"],
    }
