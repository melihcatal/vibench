import os
from google.cloud import translate_v3 as translate

def translate_caption(text_content, target_language_code, project_id=None):
    if project_id is None:
        project_id = os.environ.get("GOOGLE_CLOUD_PROJECT")
    if not project_id:
        raise ValueError("Google Cloud project ID must be provided or set in GOOGLE_CLOUD_PROJECT environment variable.")

    client = translate.TranslationServiceClient()

    parent = f"projects/{project_id}/locations/global"

    response = client.translate_text(
        request={
            "parent": parent,
            "contents": [text_content],
            "mime_type": "text/plain",
            "source_language_code": "en-US",
            "target_language_code": target_language_code,
        }
    )

    for translation in response.translations:
        return translation.translated_text
    return ""