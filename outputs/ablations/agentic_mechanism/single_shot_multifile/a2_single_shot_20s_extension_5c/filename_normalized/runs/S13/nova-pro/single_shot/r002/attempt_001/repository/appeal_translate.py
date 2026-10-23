import os
from google.cloud import translate_v2 as translate

def appeal_translate(text, target_language='es'):
    os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = 'path/to/credentials.json'
    translate_client = translate.Client()
    result = translate_client.translate(text, target_language=target_language)
    return result['translatedText']