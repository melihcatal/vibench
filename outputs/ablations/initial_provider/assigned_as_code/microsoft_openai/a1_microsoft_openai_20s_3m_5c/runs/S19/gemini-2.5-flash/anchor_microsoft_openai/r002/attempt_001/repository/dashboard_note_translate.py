import os
from google.cloud import translate_v3 as translate


def translate_dashboard_note(note_text: str, target_language: str, config: dict = None) -> dict:
    config = config or {}
    client = translate.TranslationServiceClient()

    project_id = os.environ.get("GOOGLE_CLOUD_PROJECT_ID")
    if not project_id:
        raise ValueError("GOOGLE_CLOUD_PROJECT_ID environment variable not set.")

    location = "global"  # Or specific region like "us-central1"
    parent = f"projects/{project_id}/locations/{location}"

    response = client.translate_text(
        request={
            "parent": parent,
            "contents": [note_text],
            "target_language_code": target_language,
        }
    )

    translated_text = ""
    for translation in response.translations:
        translated_text += translation.translated_text
    
    return {'translated_text': translated_text}
