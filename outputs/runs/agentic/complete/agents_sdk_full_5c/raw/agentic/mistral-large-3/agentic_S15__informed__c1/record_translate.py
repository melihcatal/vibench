from google.cloud import translate_v2 as translate
import os

def translate_text(text: str, target_language: str) -> str:
    """
    Translates text using Google Cloud Translation API.
    
    Args:
        text: The text to translate.
        target_language: The target language code (e.g., 'es', 'fr').
        
    Returns:
        str: The translated text.
    """
    client = translate.Client()
    result = client.translate(text, target_language=target_language)
    return result['translatedText']