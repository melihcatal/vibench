import os

from google.cloud import translate_v3


def dashboard_note_translate(text: str, target_language: str):
    client = translate_v3.TranslationServiceClient()
    project_id = os.environ.get("GOOGLE_CLOUD_PROJECT", "")
    parent = f"projects/{project_id}/locations/global"
    response = client.translate_text(
        request={
            "parent": parent,
            "contents": [text],
            "mime_type": "text/plain",
            "target_language_code": target_language,
        }
    )
    return response.translations[0].translated_text if response.translations else ""
