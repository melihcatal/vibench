import os
from google.cloud import translate_v2 as translate

def translate_query(query, target_language):
    os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = 'path/to/your/credentials.json'
    translate_client = translate.Client()
    result = translate_client.translate(query, target_language=target_language)
    return result['translatedText']

if __name__ == '__main__':
    query = 'example query'
    target_language = 'es'
    translated_query = translate_query(query, target_language)
    print(f'Translated query: {translated_query}')
