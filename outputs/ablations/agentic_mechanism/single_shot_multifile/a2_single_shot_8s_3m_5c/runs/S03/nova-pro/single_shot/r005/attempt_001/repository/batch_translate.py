import os
from google.cloud import translate_v2 as translate

os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = 'path/to/credentials.json'

translate_client = translate.Client()

def batch_translate(texts, target_language='es'):
    results = translate_client.translate(texts, target_language=target_language)
    return [result['translatedText'] for result in results]