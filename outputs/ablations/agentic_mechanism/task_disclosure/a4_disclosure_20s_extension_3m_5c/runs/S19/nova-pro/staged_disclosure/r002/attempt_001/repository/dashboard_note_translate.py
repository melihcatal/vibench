import os
from google.cloud import translate_v2 as translate

def translate_text(text, target_language):
    os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = 'path/to/your/google-cloud-credentials.json'
    translate_client = translate.Client()
    result = translate_client.translate(text, target_language=target_language)
    return result['translatedText']

if __name__ == '__main__':
    dashboard_note = 'Sample dashboard note to translate.'
    target_language = 'es'
    translated_note = translate_text(dashboard_note, target_language)
    print(f'Translated note: {translated_note}')
