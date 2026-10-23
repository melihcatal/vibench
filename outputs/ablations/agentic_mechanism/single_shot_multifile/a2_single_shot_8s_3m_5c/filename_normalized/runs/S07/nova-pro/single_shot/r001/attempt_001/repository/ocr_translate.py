import os
from google.cloud import translate_v2 as translate

def translate_text(text, target_language='en'):
    client = translate.Client(key=os.environ['GOOGLE_CLOUD_TRANSLATE_KEY'])
    result = client.translate(text, target_language=target_language)
    return result['translatedText']