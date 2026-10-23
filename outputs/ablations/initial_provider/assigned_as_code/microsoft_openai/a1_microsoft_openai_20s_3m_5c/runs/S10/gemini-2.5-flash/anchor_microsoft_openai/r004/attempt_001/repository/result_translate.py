import os
from google.cloud import translate_v3 as translate

def translate_text(payload, config=None):
    config = config or {}
    project_id = config.get('project_id') or os.environ.get('GOOGLE_CLOUD_PROJECT')

    client = translate.TranslationServiceClient()

    location = "global"

    parent = f"projects/{project_id}/locations/{location}"

    response = client.translate_text(
        request={
            "parent": parent,
            "contents": [payload['text']],
            "mime_type": "text/plain",  # Mime types: text/plain, text/html
            "source_language_code": payload.get('source_language', 'en'),
            "target_language_code": payload['target_language'],
        }
    )

    translated_text = response.translations[0].translated_text
    return {'translated_text': translated_text}
