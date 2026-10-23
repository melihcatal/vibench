import os
from google.cloud import translate_v2 as translate

def batch_translate(texts, target_language):
    client = translate.Client(key=os.getenv('GOOGLE_CLOUD_TRANSLATE_API_KEY'))
    results = client.translate_batch(texts, target_language=target_language)
    return [result['translatedText'] for result in results]