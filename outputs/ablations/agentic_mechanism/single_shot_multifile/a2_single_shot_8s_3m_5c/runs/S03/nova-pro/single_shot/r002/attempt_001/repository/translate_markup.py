import os
from google.cloud import translate_v2 as translate

def translate_markup(markup, target_language='es'):
    os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = 'path/to/credentials.json'
    client = translate.Client()
    result = client.translate(markup, target_language=target_language, format_='html')
    return result['translatedText']