from typing import Dict, Any
from google.cloud import translate_v2 as translate

def translate_record(document: Dict[str, Any], fields_to_translate: list, target_language: str) -> Dict[str, Any]:
    """
    Translates user-facing document fields using Google Cloud Translation API.
    """
    client = translate.Client()
    translated_doc = document.copy()
    
    for field in fields_to_translate:
        text = document.get(field, "")
        result = client.translate(text, target_language=target_language)
        translated_doc[field] = result['translatedText']
    
    return translated_doc