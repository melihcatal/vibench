import os
from google.cloud import translate_v2 as translate


def multilingual_query_translate(query, target_language='en'):
    client = translate.Client()
    result = client.translate(query, target_language=target_language)
    return {'provider': 'google-cloud-translate', 'translated_text': result['translatedText'], 'target_language': target_language}
