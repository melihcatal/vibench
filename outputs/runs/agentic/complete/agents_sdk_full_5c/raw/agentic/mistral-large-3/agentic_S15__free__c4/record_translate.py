from typing import Dict, Any
from google.cloud import translate_v2 as translate
import os

GOOGLE_APPLICATION_CREDENTIALS = os.getenv("GOOGLE_APPLICATION_CREDENTIALS", "your-google-credentials.json")

client = translate.Client()

def translate_text(text: str, target_language: str = "en") -> str:
    """
    Translates text using Google Cloud Translation API.
    """
    result = client.translate(text, target_language=target_language)
    return result['translatedText']

def translate_document_fields(document: Dict[str, Any], fields: list, target_language: str = "en") -> Dict[str, Any]:
    """
    Translates specified fields in a document using Google Cloud Translation API.
    """
    translated_doc = document.copy()
    for field in fields:
        if field in document:
            translated_doc[field] = translate_text(str(document[field]), target_language)
    return translated_doc