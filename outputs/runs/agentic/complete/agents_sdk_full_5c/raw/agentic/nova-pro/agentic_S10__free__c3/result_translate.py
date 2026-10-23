import os
from google.cloud import translate_v2 as translate

def translate_text(text, target_language):
    client = translate.Client(os.getenv('GOOGLE_CLOUD_API_KEY'))
    result = client.translate(text, target_language=target_language)
    return result['translatedText']