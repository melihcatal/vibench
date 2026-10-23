import os
from google.cloud import translate_v3 as translate

def translate_text_field(text: str, target_language: str = "es", project_id: str = None) -> str:
    if project_id is None:
        project_id = os.environ.get('GOOGLE_CLOUD_PROJECT_ID')
    if not project_id:
        raise ValueError("Google Cloud Project ID must be provided or set in GOOGLE_CLOUD_PROJECT_ID environment variable.")

    client = translate.TranslationServiceClient()
    location = "global"
    parent = f"projects/{project_id}/locations/{location}"

    response = client.translate_text(
        request={
            "parent": parent,
            "contents": [text],
            "mime_type": "text/plain",
            "source_language_code": "en",
            "target_language_code": target_language,
        }
    )

    if response.translations:
        return response.translations[0].translated_text
    return text