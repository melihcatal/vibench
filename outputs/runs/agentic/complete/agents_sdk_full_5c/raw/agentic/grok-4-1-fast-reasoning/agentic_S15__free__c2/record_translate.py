from google.cloud import translate_v2 as translate
from typing import Dict, Any, List, Optional

def translate_document_fields(document: Dict[str, Any], target_language: str = 'en', fields: Optional[List[str]] = None) -> Dict[str, Any]:
    client = translate.Client()
    translated_doc = document.copy()
    target_fields = fields or [k for k, v in document.items() if isinstance(v, str)]
    for field in target_fields:
        if field in document and isinstance(document[field], str):
            result = client.translate(document[field], target_language=target_language)
            translated_doc[field] = result['translatedText']
    return translated_doc