import os
from google.cloud import translate_v2 as translate

def result_translate(payload, config=None):
    config = config or {}
    project_id = config.get('project_id') or os.environ.get('GOOGLE_CLOUD_PROJECT')
    target_language = payload.get('target_language', 'es') # Default to Spanish

    client = translate.Client(project=project_id)

    # Text can also be a list of strings, in which case a list of translations is returned.
    translation = client.translate(
        payload['text'],
        target_language=target_language
    )

    return {
        'translated_text': translation['translatedText'],
        'original_text': translation['input'],
        'source_language': translation['detectedSourceLanguage'],
        'target_language': target_language
    }
