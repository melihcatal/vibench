import os
from typing import Dict, Any
from google.cloud import translate_v2 as translate


def translate_invoice_note(text: str, target_language: str = "en") -> Dict[str, Any]:
    client = translate.Client()

    if not text:
        return {"original_text": text, "translated_text": "", "detected_source_language": "", "provider": "Google Cloud Translation"}

    result = client.translate(text, target_language=target_language)

    return {"original_text": text,
            "translated_text": result["translatedText"],
            "detected_source_language": result["detectedSourceLanguage"],
            "provider": "Google Cloud Translation"}