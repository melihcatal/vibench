import os
from google.cloud import translate_v2 as translate

def translate_alt_text(text: str, target_language: str = 'es') -> str:
    """
    Translates generated image descriptions using Google Cloud Translation API.

    Args:
        text: The text to translate.
        target_language: The target language code (e.g., 'es' for Spanish, 'fr' for French).

    Returns:
        The translated text.
    """
    client = translate.Client()
    
    result = client.translate(
        text,
        target_language=target_language
    )
    
    return result['translatedText']
