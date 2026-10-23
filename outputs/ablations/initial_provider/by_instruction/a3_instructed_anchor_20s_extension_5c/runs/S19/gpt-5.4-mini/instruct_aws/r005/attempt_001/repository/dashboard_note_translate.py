import os

from google.cloud import translate_v3 as translate


def dashboard_note_translate(text: str, target_language: str, project_id: str = None, location: str = "global"):
    project_id = project_id or os.getenv("GOOGLE_CLOUD_PROJECT")
    client = translate.TranslationServiceClient()
    parent = f"projects/{project_id}/locations/{location}"
    response = client.translate_text(contents=[text], target_language_code=target_language, parent=parent, mime_type="text/plain")
    return {"provider": "google_translate_v3", "translated_text": response.translations[0].translated_text if response.translations else ""}
