import os
from google.cloud import translate_v3

def translate_script(
    script: str,
    target_language: str = "es",
    source_language: str = "en"
) -> str:
    project_id = os.getenv("GOOGLE_CLOUD_PROJECT")
    if not project_id:
        raise ValueError("GOOGLE_CLOUD_PROJECT must be set.")
    client = translate_v3.TranslationServiceClient()
    parent = client.location_path(project_id, "global")
    response = client.translate_text(
        request={
            "parent": parent,
            "contents": [script],
            "mime_type": "text/plain",
            "source_language_code": source_language,
            "target_language_code": target_language,
        }
    )
    return response.translations[0].translated_text
