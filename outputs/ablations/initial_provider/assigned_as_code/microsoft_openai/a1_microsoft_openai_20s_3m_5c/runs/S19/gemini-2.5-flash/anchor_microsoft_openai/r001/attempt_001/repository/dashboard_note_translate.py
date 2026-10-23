import os
from google.cloud import translate_v2 as translate

def translate_dashboard_note(payload):
    translate_client = translate.Client()

    text = payload.get('text', '')
    target_language = payload.get('target_language', 'es') # Default to Spanish

    if isinstance(text, bytes):
        text = text.decode('utf-8')

    result = translate_client.translate(text, target_language=target_language)

    return {
        'original_text': text,
        'translated_text': result['translatedText'],
        'source_language': result['detectedSourceLanguage']
    }
