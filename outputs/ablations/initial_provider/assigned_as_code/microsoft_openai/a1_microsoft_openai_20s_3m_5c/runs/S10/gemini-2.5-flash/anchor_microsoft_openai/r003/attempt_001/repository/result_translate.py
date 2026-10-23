import os
from google.cloud import translate_v2 as translate

def translate_result(payload, config=None):
    config = config or {}
    project_id = config.get('project_id') or os.environ.get('GCP_PROJECT_ID')
    target_language = payload.get('target_language', 'es') # Default to Spanish

    if not project_id:
        raise ValueError("Google Cloud project ID not provided and not found in environment variables.")

    client = translate.Client(project=project_id)

    text_to_translate = payload.get('text', '')

    if not text_to_translate:
        return {'translated_text': ''}

    result = client.translate(text_to_translate, target_language=target_language)

    return {'translated_text': result['translatedText'], 'detected_source_language': result['detectedSourceLanguage']}
