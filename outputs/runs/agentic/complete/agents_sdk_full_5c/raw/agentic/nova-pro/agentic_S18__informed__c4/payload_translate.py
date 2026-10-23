import os
from google.cloud import translate_v2 as translate

os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = 'path-to-your-service-account-file.json'

client = translate.Client()

def translate_message(message, target_language='en'):
    result = client.translate(message, target_language=target_language)
    return result['translatedText']