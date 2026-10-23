import os
from google.cloud import translate_v2 as translate

def translate_text(text, target_language):
    os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = 'path/to/your/credentials.json'
    translate_client = translate.Client()
    result = translate_client.translate(text, target_language=target_language)
    return result['translatedText']

if __name__ == '__main__'):
    text = 'Sample transcript segment to translate.'
    target_language = 'es'
    translated_text = translate_text(text, target_language)
    print(f'Translated text: {translated_text}')
