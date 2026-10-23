import os
from google.cloud import translate_v2 as translate

def translate_text(text, target_language='en'):
    os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = 'path_to_your_service_account_file.json'
    translate_client = translate.Client()
    result = translate_client.translate(text, target_language=target_language)
    return result['translatedText']

if __name__ == '__main__':
    note = 'Your encryption or compliance note here'
    translated_note = translate_text(note)
    print(f'Translated Note: {translated_note}')
