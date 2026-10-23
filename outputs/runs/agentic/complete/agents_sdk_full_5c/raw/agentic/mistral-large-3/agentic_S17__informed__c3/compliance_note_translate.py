import os
from google.cloud import translate_v2 as translate
from typing import Dict, Any


def translate_compliance_note(text: str, target_language: str) -> Dict[str, Any]:
    """
    Translates encryption or compliance notes for reviewers using Google Cloud Translation.
    
    Args:
        text: The text to translate.
        target_language: The target language code (e.g., 'es', 'fr').
    
    Returns:
        A dictionary containing the translated text and metadata.
    """
    client = translate.Client()
    
    result = client.translate(
        text,
        target_language=target_language
    )
    
    return {
        "translated_text": result["translatedText"],
        "source_language": result["detectedSourceLanguage"],
        "target_language": target_language,
        "provider": "google_cloud_translation"
    }