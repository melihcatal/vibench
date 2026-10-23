from typing import Dict, Any
from google.cloud import translate_v2 as translate
from database_models import DocumentResponse

# Initialize Google Cloud Translate client
translate_client = translate.Client.from_service_account_json("path/to/service-account.json")

def translate_document(document: DocumentResponse, target_language: str = "es") -> Dict[str, Any]:
    """
    Translates user-facing document fields using Google Cloud Translation API.
    
    Args:
        document: The document to translate.
        target_language: The target language code (e.g., 'es' for Spanish).
        
    Returns:
        A dictionary with translated fields.
    """
    translated_data = {}
    for key, value in document.data.items():
        if isinstance(value, str):
            result = translate_client.translate(value, target_language=target_language)
            translated_data[key] = result["translatedText"]
        else:
            translated_data[key] = value
    return translated_data