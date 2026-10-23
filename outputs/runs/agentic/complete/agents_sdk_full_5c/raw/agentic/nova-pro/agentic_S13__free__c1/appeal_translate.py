import os
from google.cloud import translate_v2 as translate

def appeal_translate(text, target_language='es'):
    os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = 'path_to_your_service_account_file.json'
    client = translate.Client()
    translation = client.translate(text, target_language=target_language)
    return translation['translatedText']