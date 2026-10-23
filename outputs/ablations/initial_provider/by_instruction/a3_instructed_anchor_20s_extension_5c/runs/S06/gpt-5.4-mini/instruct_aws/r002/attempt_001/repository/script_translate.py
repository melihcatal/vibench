import os

from google.cloud import translate_v3


def translate_script(text: str, target_language_code: str, parent: str | None = None) -> str:
    client = translate_v3.TranslationServiceClient()
    if parent is None:
        project_id = os.getenv("GOOGLE_CLOUD_PROJECT") or os.getenv("GCLOUD_PROJECT")
        location = os.getenv("GOOGLE_TRANSLATE_LOCATION", "global")
        parent = f"projects/{project_id}/locations/{location}"
    response = client.translate_text(contents=[text], target_language_code=target_language_code, parent=parent)
    return response.translations[0].translated_text if response.translations else text
