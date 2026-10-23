import os
from google.cloud import translate_v2 as translate

def alt_text_translate(description: str, target_lang: str = 'es') -> str:
    """Translate the generated image description to another language using Google Cloud Translation API.
    Returns the translated caption.
    """
    client = translate.Client()
    result = client.translate(description, target_language=target_lang)
    return result['translatedText']
