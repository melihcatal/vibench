from __future__ import annotations

import os
from google.cloud import translate_v3 as translate


def translate_script(text: str, target_language: str, source_language: str | None = None) -> str:
    client = translate.TranslationServiceClient()
    project_id = os.getenv('GOOGLE_CLOUD_PROJECT') or os.getenv('GCP_PROJECT')
    location = os.getenv('GOOGLE_CLOUD_LOCATION', 'global')
    parent = f'projects/{project_id}/locations/{location}' if project_id else f'locations/{location}'
    response = client.translate_text(
        request={
            'parent': parent,
            'contents': [text],
            'mime_type': 'text/plain',
            'source_language_code': source_language,
            'target_language_code': target_language,
        }
    )
    return response.translations[0].translated_text if response.translations else ''
