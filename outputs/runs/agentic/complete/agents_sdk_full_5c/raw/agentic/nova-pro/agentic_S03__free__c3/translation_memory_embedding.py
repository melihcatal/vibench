import os
from google.cloud import translate_v2 as translate

def embed_translation_memory(text):
    os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = 'path/to/credentials.json'
    translate_client = translate.Client()
    result = translate_client.translate(text)
    return result['data']['translations'][0]['translatedText']