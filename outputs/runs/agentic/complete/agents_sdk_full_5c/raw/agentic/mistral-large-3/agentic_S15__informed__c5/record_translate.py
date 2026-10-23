import os
from typing import Dict, Any
from google.cloud import translate_v2 as translate

def translate_record(document: Dict[str, Any], target_language: str) -> Dict[str, Any]:
    """
    Translates user-facing document fields using Google Cloud Translation.
    """
    client = translate.Client()
    translated_doc = document.copy()
    
    for field, value in document.items():
        if isinstance(value, str) and len(value) > 0:
            result = client.translate(value, target_language=target_language)
            translated_doc[field] = result['translatedText']
    
    return translated_doc