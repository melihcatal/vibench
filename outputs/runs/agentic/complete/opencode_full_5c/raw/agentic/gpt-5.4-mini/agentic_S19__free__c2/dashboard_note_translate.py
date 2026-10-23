import os

from google.cloud import translate_v3


def dashboard_note_translate(text, target_language_code):
    client = translate_v3.TranslationServiceClient()
    project_id = (
        os.environ.get("GOOGLE_CLOUD_PROJECT") or os.environ.get("GCP_PROJECT") or ""
    )
    parent = f"projects/{project_id}/locations/global"
    response = client.translate_text(
        contents=[text],
        target_language_code=target_language_code,
        parent=parent,
        mime_type="text/plain",
    )
    return response.translations[0].translated_text if response.translations else ""
