import os
from google.cloud import translate_v2 as translate

translate_client = translate.Client(credentials=os.getenv('GOOGLE_APPLICATION_CREDENTIALS'))

def translate_query(query, target_language):
    response = translate_client.translate(query, target_language=target_language)
    return response['translatedText']