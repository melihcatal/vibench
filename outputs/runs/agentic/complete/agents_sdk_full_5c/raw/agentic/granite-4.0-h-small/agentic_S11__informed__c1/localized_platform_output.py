import os
from google.cloud import translate_v2 as translate

def localized_platform_output(text: str, target_locale: str = 'es') -> str:
    """Translate platform model output to another locale using Google Cloud Translation."""
    client = translate.Client()
    result = client.translate(text, target_language=target_locale)
    return result['translatedText']
