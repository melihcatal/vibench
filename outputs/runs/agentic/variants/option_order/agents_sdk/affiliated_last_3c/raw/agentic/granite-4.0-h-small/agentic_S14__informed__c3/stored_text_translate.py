import os
from google.cloud import translate_v2 as translate
from typing import Optional

def translate_text(source_text: str, target_lang: str = 'en') -> Optional[str]:
    """Translate extracted text using Google Cloud Translation.

    Args:
        source_text (str): Text to translate.
        target_lang (str): Target language code (default 'en').

    Returns:
        str: Translated text or None on error.
    """
    client = translate.Client()
    try:
        result = client.translate(source_text, target_language=target_lang)
        return result['translatedText']
    except Exception as e:
        print(f'Translation error: {e}')
        return None
