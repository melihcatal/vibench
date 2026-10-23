import os
from google.cloud import translate_v2 as translate

def translate_text(text, target_language='es'):
    os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = 'path/to/credentials.json'
    client = translate.Client()
    result = client.translate(text, target_language=target_language)
    return result['translatedText']