import os
from google.cloud import translate_v3 as translate

client = translate.TranslationServiceClient()

def translate_text(source_text: str, target_lang: str = 'en') -> str:
    name = os.getenv('TRANSLATION_MODEL') or 'projects/{}/locations/global/models/default'.format(os.getenv('GOOGLE_CLOUD_PROJECT'))
    parent = f'projects/{os.getenv("GOOGLE_CLOUD_PROJECT")}/locations/global'
    response = client.translate_text(
        request={
            'parent': parent,
            'contents': [source_text],
            'mime_type': 'text/plain',
            'target_language_code': target_lang,
            'model': name
        }
    )
    return response.translations[0].translated_text
