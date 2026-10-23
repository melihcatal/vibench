import os
from typing import Dict, Any, List
from google.cloud import translate_v2 as translate

client = translate.Client()

def record_translate(documents: List[Dict[str, Any]], target_language: str = 'en') -> List[Dict[str, Any]]:
    translated_docs = []
    for doc in documents:
        translated = {}
        for k, v in doc.items():
            if isinstance(v, str):
                result = client.translate(v, target_language=target_language)
                translated[k] = result['translatedText']
            else:
                translated[k] = v
        translated_docs.append(translated)
    return translated_docs
