import os
from google.cloud import translate_v2 as translate

def translate_consent_copy(text: str, target_language: str) -> str:
    if not os.environ.get("GOOGLE_APPLICATION_CREDENTIALS"):
        raise ValueError("GOOGLE_APPLICATION_CREDENTIALS environment variable not set.")

    translate_client = translate.Client()

    result = translate_client.translate(text, target_language=target_language)
    
    return result['translatedText']
