import os
from google.cloud import translate_v2 as translate
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = 'your_service_account_file.json'

def translate_text(text, target_language='en'):
    translate_client = translate.Client()
    result = translate_client.translate(text, target_language=target_language)
    return result['translatedText']