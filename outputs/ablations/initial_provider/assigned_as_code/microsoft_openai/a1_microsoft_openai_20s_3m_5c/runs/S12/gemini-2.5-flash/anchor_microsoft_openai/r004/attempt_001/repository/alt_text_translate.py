from google.cloud import translate_v2 as translate
import os

def alt_text_translate(payload, config=None):
    config = config or {}
    translate_client = translate.Client()

    text_to_translate = payload.get('text', '')
    target_language = config.get('target_language', 'es') # Default to Spanish

    if not text_to_translate:
        return {'translated_text': ''}

    result = translate_client.translate(text_to_translate, target_language=target_language)

    return {'translated_text': result['translatedText']}
