import os
from google.cloud import translate_v3 as translate

def translate_query(text: str, target_language_code: str, project_id: str = None) -> str:
    client = translate.TranslationServiceClient()

    if project_id is None:
        project_id = os.getenv("GOOGLE_CLOUD_PROJECT")
        if not project_id:
            raise ValueError("GOOGLE_CLOUD_PROJECT environment variable not set or project_id not provided.")

    location = "global"
    parent = f"projects/{project_id}/locations/{location}"

    response = client.translate_text(
        request={
            "parent": parent,
            "contents": [text],
            "target_language_code": target_language_code,
            "mime_type": "text/plain",
        }
    )
    return response.translations[0].translated_text
