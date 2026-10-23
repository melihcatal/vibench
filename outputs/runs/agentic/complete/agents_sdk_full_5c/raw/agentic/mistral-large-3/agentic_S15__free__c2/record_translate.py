from typing import Dict, Any
from google.cloud import translate_v2 as translate

def translate_record(document: Dict[str, Any], field_name: str = "content", target_language: str = "es") -> Dict[str, Any]:
    """
    Translates user-facing document fields using Google Cloud Translation API.
    """
    client = translate.Client()
    content = document.get(field_name, "")
    
    if not content:
        return document

    result = client.translate(content, target_language=target_language)
    translated_doc = document.copy()
    translated_doc[f"{field_name}_translated"] = result["translatedText"]
    return translated_doc