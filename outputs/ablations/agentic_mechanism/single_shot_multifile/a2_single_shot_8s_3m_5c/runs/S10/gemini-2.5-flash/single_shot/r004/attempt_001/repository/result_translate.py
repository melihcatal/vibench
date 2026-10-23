import os
from google.cloud import translate_v3 as translate

def translate_output(text: str, target_language_code: str = "es", project_id: str = None) -> str:
    client = translate.TranslationServiceClient()

    if project_id is None:
        project_id = os.getenv("GOOGLE_CLOUD_PROJECT")
    if not project_id:
        raise ValueError("Google Cloud Project ID not provided and GOOGLE_CLOUD_PROJECT environment variable not set.")

    parent = f"projects/{project_id}"

    response = client.translate_text(
        request={
            "parent": parent,
            "contents": [text],
            "target_language_code": target_language_code,
        }
    )

    translated_text = ""
    if response.translations:
        translated_text = response.translations[0].translated_text
    
    return translated_text
