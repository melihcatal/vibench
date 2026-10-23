import os
from google.cloud import translate_v2 as translate

def get_translate_client():
    os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = 'path/to/your/credentials.json'
    return translate.Client()

def translate_text(client, text, target_language):
    result = client.translate(text, target_language=target_language)
    return result['translatedText']