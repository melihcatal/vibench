import os
from google.cloud import translate_v2 as translate

def summarize_translation_quality(text, target_lang='EN'):
    os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = 'path/to/credentials.json'
    translate_client = translate.Client()
    result = translate_client.translate(text, target_language=target_lang)
    return result['detectedSourceLanguage'], result['translatedText']