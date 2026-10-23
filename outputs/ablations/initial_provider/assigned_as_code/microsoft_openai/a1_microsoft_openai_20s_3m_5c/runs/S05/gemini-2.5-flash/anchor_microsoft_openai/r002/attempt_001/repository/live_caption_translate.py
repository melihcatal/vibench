import os
from google.cloud import translate

def translate_caption(text: str, target_language_code: str, project_id: str = None) -> str:
    if project_id is None:
        project_id = os.environ.get("GCP_PROJECT_ID")
    if not project_id:
        raise ValueError("Google Cloud Project ID must be provided or set in GCP_PROJECT_ID environment variable.")

    client = translate.TranslationServiceClient()
    location = "global"
    parent = f"projects/{project_id}/locations/{location}"

    response = client.translate_text(
        request={
            "parent": parent,
            "contents": [text],
            "target_language_code": target_language_code,
        }
    )

    translated_text = ""
    for translation in response.translations:
        translated_text += translation.translated_text
    
    return translated_text
