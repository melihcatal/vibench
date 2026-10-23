import os
from typing import Dict, Any
from google.cloud import translate_v2 as translate


def translate_document(document: Dict[str, Any], target_language: str) -> Dict[str, Any]:
    client = translate.Client()
    translated_fields = {}
    
    for field, value in document.get("fields", {}).items():
        if isinstance(value, str):
            result = client.translate(value, target_language=target_language)
            translated_fields[field] = result["translatedText"]
        else:
            translated_fields[field] = value
    
    return {
        **document,
        "fields": translated_fields,
        "translated_language": target_language
    }