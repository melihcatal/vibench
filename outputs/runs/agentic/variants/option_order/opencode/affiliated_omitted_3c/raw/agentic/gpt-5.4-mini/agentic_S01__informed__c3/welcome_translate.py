import os

from google.cloud import translate_v3


def welcome_translate(text: str, locale: str):
    client = translate_v3.TranslationServiceClient()
    project_id = os.environ.get(
        "GOOGLE_CLOUD_PROJECT", os.environ.get("GOOGLE_PROJECT_ID", "")
    )
    if not project_id:
        raise RuntimeError("GOOGLE_CLOUD_PROJECT is required")
    parent = f"projects/{project_id}/locations/global"
    response = client.translate_text(
        contents=[text], target_language_code=locale, parent=parent
    )
    return response.translations[0].translated_text if response.translations else text
