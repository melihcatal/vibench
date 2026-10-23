import os
from google.cloud import translate_v2 as translate
from safety_models import ModSafetyResponse

def appeal_translate_google(appeal_text: str, target_lang: str = 'en') -> ModSafetyResponse:
    """Translate an appeal message using Google Cloud Translation.
    Returns the provider's raw JSON response.
    """
    client = translate.Client()
    result = client.translate(appeal_text, target_language=target_lang)
    return {'provider': 'Google Translation', 'raw_response': result}

__all__ = ['appeal_translate_google']
