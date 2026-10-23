from typing import Dict, Any
from google.cloud import translate_v2 as translate

def translate_record(document: Dict[str, Any], target_language: str = "es") -> Dict[str, Any]:
    """
    Translates user-facing document fields using Google Cloud Translation API.
    """
    translate_client = translate.Client()
    translated_document = {}
    
    for key, value in document.items():
        if isinstance(value, str):
            result = translate_client.translate(value, target_language=target_language)
            translated_document[key] = result["translatedText"]
        else:
            translated_document[key] = value
    
    return translated_document