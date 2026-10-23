import os
from google.cloud import translate_v2 as translate
from typing import Dict, Any, Optional


def get_translate_client():
    """Initialize and return the Google Cloud Translation client." ""
    return translate.Client.from_service_account_json(os.getenv("GOOGLE_APPLICATION_CREDENTIALS"))


def translate_text(text: str, target_language: str = "es") -> str:
    """
    Translates user-facing document fields using Google Cloud Translation.
    
    Args:
        text: The text to translate.
        target_language: The target language code (default: "es").
        
    Returns:
        The translated text.
    """
    client = get_translate_client()
    result = client.translate(text, target_language=target_language)
    return result["translatedText"]


def translate_document_fields(document: Dict[str, Any], fields: List[str], target_language: str = "es") -> Dict[str, Any]:
    """
    Translates specified fields in a document.
    
    Args:
        document: The document containing fields to translate.
        fields: The list of field names to translate.
        target_language: The target language code (default: "es").
        
    Returns:
        The document with translated fields.
    """
    client = get_translate_client()
    translated_document = document.copy()
    
    for field in fields:
        if field in document:
            translated_document[field] = translate_text(document[field], target_language)
    
    return translated_document