import os

from google.cloud import translate_v3 as translate


def dashboard_note_translate(payload, config=None):
    config = config or {}
    project_id = config.get("project_id") or os.environ.get("GOOGLE_CLOUD_PROJECT") or os.environ.get("GCLOUD_PROJECT")
    if not project_id:
        raise ValueError("project_id is required")
    client = translate.TranslationServiceClient()
    parent = f"projects/{project_id}/locations/global"
    response = client.translate_text(request={"parent": parent, "contents": [payload["text"]], "mime_type": "text/plain", "target_language_code": payload["target_language"]})
    return {"text": response.translations[0].translated_text if response.translations else ""}
