import os
from google.cloud import translate

def translate_text(text, target_language):
    os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = 'path/to/credentials.json'
    client = translate.TranslateClient()
    translation = client.translate(text, target_language=target_language)
    return translation['translatedText']

if __name__ == '__main__':
    note = 'Sample dashboard note'
    translated_note = translate_text(note, 'es')
    print(f'Translated note: {translated_note}')
