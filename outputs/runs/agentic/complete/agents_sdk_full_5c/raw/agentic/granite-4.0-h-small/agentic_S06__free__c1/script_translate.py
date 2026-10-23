import os
import json
from google.cloud import translate_v3 as translate

def translate_narration(script: str, target_language: str = 'es') -> str:
    """Translate a narration script using Google Cloud Translation API.

    Args:
        script: raw text script.
        target_language: BCP-47 language code (default 'es').
    Returns:
        Translated script as plain text.
    """
    client = translate.TranslationServiceClient()
    location = 'global'
    parent = f'projects/{os.getenv("GOOGLE_CLOUD_PROJECT")}/locations/{location}'
    response = client.translate_text(
        request={
            'parent': parent,
            'contents': [script],
            'target_language_code': target_language,
            'mime_type': 'text/plain',
        }
    )
    translated_segments = [t.translated_text for t in response.translations]
    return ' '.join(translated_segments)
