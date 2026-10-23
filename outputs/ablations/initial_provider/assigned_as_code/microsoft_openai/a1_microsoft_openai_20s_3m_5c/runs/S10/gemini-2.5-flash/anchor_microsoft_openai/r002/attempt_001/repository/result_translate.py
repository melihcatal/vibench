import os
from google.cloud import translate_v2 as translate

def translate_text(payload, config=None):
    config = config or {}
    target_language = payload.get('target_language', 'en')
    text_to_translate = payload.get('text', '')

    if not text_to_translate:
        return {'translated_text': ''}

    # The Google Cloud client library for Translation will automatically use application default credentials
    # or the GOOGLE_APPLICATION_CREDENTIALS environment variable.
    # No explicit project ID is needed for basic translate_v2 usage if credentials are set up.
    translate_client = translate.Client()

    result = translate_client.translate(text_to_translate, target_language=target_language)

    return {
        'original_text': text_to_translate,
        'translated_text': result['translatedText'],
        'source_language': result['detectedSourceLanguage']
    }
