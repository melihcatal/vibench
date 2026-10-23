import os
from google.cloud import translate_v2 as translate

def translate_markup(text, target_language):
    os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = 'path/to/credentials.json'
    client = translate.Client()
    result = client.translate(text, target_language=target_language, format_='html')
    return result['translatedText']