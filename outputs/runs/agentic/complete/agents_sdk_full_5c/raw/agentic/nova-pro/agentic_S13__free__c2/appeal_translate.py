import os
from google.cloud import translate_v2 as translate

def translate_appeal(text, target_language='en'):
    client = translate.Client(os.getenv('GOOGLE_CLOUD_KEY'))
    result = client.translate(text, target_language=target_language)
    return result['translatedText']