import os

from google.cloud import translate_v3


def script_translate(payload, config=None):
    data = dict(payload or {})
    client = translate_v3.TranslationServiceClient()
    project_id = data.get("project_id") or os.getenv("GOOGLE_CLOUD_PROJECT")
    location = data.get("location", "global")
    parent = f"projects/{project_id}/locations/{location}"
    response = client.translate_text(
        parent=parent,
        contents=[data["text"]],
        mime_type="text/plain",
        target_language_code=data.get("target_language", "en"),
    )
    return {"translated_text": response.translations[0].translated_text}
