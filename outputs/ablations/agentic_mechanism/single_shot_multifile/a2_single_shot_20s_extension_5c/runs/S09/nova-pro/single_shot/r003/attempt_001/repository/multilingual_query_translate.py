import os
from google.cloud import translate_v2 as translate

translate_client = translate.Client(os.getenv('GOOGLE_CLOUD_API_KEY'))

def translate_query(query, target_language):
    translation = translate_client.translate(query, target_language=target_language)
    return translation['translatedText']