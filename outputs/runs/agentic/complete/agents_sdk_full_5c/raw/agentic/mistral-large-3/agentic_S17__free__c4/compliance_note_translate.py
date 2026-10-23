import os
from google.cloud import translate_v2 as translate
from typing import Dict


def translate_compliance_note(note: str, target_language: str = "es") -> Dict[str, str]:
    client = translate.Client()
    
    result = client.translate(
        note,
        target_language=target_language,
        source_language="en"
    )
    
    return {
        "original_text": note,
        "translated_text": result["translatedText"],
        "detected_source_language": result["detectedSourceLanguage"],
        "target_language": target_language
    }