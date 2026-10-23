import os
from google.cloud import translate_v2 as translate

def translate_text(text, target_language):
    os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = 'path/to/your/google-cloud-credentials.json'
    client = translate.Client()
    result = client.translate(text, target_language=target_language)
    return result['translatedText']

if __name__ == '__main__':
    text_to_translate = 'Your query text here'
    target_language = 'es'  # Example: Spanish
    translated_text = translate_text(text_to_translate, target_language)
    print(f'Translated text: {translated_text}')
