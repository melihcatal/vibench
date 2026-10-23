from google.cloud import translate_v2 as translate
from translation_client import translate_client

def batch_translate(texts, target_language):
    client = translate_client()
    results = client.translate(texts, target_language=target_language)
    return [result['translatedText'] for result in results]