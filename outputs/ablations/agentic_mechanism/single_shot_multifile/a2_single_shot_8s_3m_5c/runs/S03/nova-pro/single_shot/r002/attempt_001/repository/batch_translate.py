import os
from google.cloud import translate_v2 as translate

def batch_translate(texts, target_language='es'):
    os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = 'path/to/credentials.json'
    client = translate.Client()
    results = client.translate(texts, target_language=target_language)
    return [result['translatedText'] for result in results]