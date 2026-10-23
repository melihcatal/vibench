import os
from google.cloud import translate_v3 as translate

from document_models import normalize_response_text


PROJECT_ID = os.environ.get('GOOGLE_CLOUD_PROJECT', '')
LOCATION = os.environ.get('GOOGLE_TRANSLATE_LOCATION', 'global')


def translate_ocr_text(text: str, target_language: str, source_language: str | None = None) -> str:
    client = translate.TranslationServiceClient()
    parent = f'projects/{PROJECT_ID}/locations/{LOCATION}'
    response = client.translate_text(request={'parent': parent, 'contents': [normalize_response_text(text)], 'target_language_code': target_language, 'mime_type': 'text/plain', 'source_language_code': source_language or ''})
    return response.translations[0].translated_text if response.translations else ''
