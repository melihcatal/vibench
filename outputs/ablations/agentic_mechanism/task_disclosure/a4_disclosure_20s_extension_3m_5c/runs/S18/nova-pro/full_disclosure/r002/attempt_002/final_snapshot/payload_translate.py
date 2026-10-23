import os
from google.cloud import translate_v2 as translate

def translate_text(text, target_language='en'):
    os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = 'path/to/your/credentials.json'
    client = translate.Client()
    result = client.translate(text, target_language=target_language)
    return result['translatedText']

if __name__ == '__main__':
    sample_text = 'Hello, world!'
    translated_text = translate_text(sample_text)
    print(f'Translated text: {translated_text}')
