import os
from google.cloud import translate_v2 as translate

GOOGLE_APPLICATION_CREDENTIALS = os.getenv('GOOGLE_APPLICATION_CREDENTIALS')

def translate_consent(text, target_language='es'):
    client = translate.Client()
    result = client.translate(text, target_language=target_language)
    return result['translatedText']