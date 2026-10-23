import os
from google.cloud import translate_v2 as translate

def translate_log_message(message, target_language):
    os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = 'path/to/your/service-account-file.json'
    translate_client = translate.Client()
    result = translate_client.translate(message, target_language=target_language)
    return result['translatedText']