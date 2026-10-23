import os
from google.cloud import translate_v3

def translate_appeal_text(text: str, target_language_code: str = "en", project_id: str = None) -> str:
    if project_id is None:
        project_id = os.environ.get("GOOGLE_CLOUD_PROJECT")
        if not project_id:
            raise ValueError("Google Cloud Project ID must be provided or set in GOOGLE_CLOUD_PROJECT environment variable.")

    client = translate_v3.TranslationServiceClient()
    location = "global"

    parent = f"projects/{project_id}/locations/{location}"

    response = client.translate_text(
        request={
            "parent": parent,
            "contents": [text],
            "target_language_code": target_language_code,
        }
    )

    if response.translations:
        return response.translations[0].translated_text
    return text