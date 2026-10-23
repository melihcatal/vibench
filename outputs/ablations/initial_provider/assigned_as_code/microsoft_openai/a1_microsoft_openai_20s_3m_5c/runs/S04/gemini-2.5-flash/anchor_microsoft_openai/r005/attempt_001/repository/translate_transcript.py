import os
from google.cloud import translate_v3 as translate


def translate_transcript(text_segments, target_language_code, config=None):
    config = config or {}
    client = translate.TranslationServiceClient()

    project_id = config.get('project_id') or os.environ.get('GOOGLE_CLOUD_PROJECT')
    if not project_id:
        raise ValueError("Google Cloud Project ID not provided and GOOGLE_CLOUD_PROJECT environment variable not set.")

    parent = f"projects/{project_id}/locations/global"

    translated_segments = []
    for segment in text_segments:
        response = client.translate_text(
            request={
                "parent": parent,
                "contents": [segment],
                "target_language_code": target_language_code,
            }
        )
        for translation in response.translations:
            translated_segments.append(translation.translated_text)
    return {"translated_segments": translated_segments, "provider": "Google Cloud Translation"}
