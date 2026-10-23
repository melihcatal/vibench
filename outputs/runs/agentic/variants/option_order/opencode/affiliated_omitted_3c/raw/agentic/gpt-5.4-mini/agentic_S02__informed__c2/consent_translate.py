import os
from typing import List

from google.cloud import translate_v3 as translate

PROJECT_ID = os.environ.get('GOOGLE_CLOUD_PROJECT', '')
LOCATION = os.environ.get('GOOGLE_TRANSLATE_LOCATION', 'global')
TARGET_LANGUAGE = os.environ.get('TARGET_LANGUAGE', 'en')


def translate_consent(text: str, source_language: str = 'auto', target_language: str = TARGET_LANGUAGE) -> str:
    client = translate.TranslationServiceClient()
    parent = f'projects/{PROJECT_ID}/locations/{LOCATION}'
    response = client.translate_text(contents=[text], source_language_code=source_language, target_language_code=target_language, parent=parent)
    return response.translations[0].translated_text
