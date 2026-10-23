import os
from google.cloud import translate_v2 as translate

translate_client = translate.Client(os.getenv('GOOGLE_APPLICATION_CREDENTIALS'))

def translate_query(text, target_language):
    result = translate_client.translate(text, target_language=target_language)
    return result['translatedText']