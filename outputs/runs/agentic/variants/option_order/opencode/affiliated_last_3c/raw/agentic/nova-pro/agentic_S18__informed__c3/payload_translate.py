import os
from google.cloud import translate_v2 as translate

# Google Cloud Translation configuration
GOOGLE_APPLICATION_CREDENTIALS = os.getenv('GOOGLE_APPLICATION_CREDENTIALS')

def translate_text(text, target_language='en'):
    translate_client = translate.Client()
    result = translate_client.translate(text, target_language=target_language)
    return result['translatedText']

if __name__ == '__main__':
    text = 'Hello, world!'
    translated_text = translate_text(text)
    print(f'Translated text: {translated_text}