import os
from google.cloud import translate_v2 as translate

def batch_translate(texts, target_language):
    os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = 'path/to/your/google-credentials.json'
    client = translate.Client()
    results = client.translate(texts, target_language=target_language)
    return [result['translatedText'] for result in results['data']['translations']]

if __name__ == '__main__':\n    texts = ['Hello', 'world']
    target_language = 'es'
    translated_texts = batch_translate(texts, target_language)
    print(translated_texts)