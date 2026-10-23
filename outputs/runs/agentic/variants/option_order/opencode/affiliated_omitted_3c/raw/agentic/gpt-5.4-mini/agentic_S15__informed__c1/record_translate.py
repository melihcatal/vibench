import os

from google.cloud import translate_v3 as translate


def translate_text(text, target_language_code, parent=None):
    client = translate.TranslationServiceClient()
    project_id = os.getenv("GOOGLE_CLOUD_PROJECT")
    if parent is None:
        parent = f"projects/{project_id}/locations/global"
    response = client.translate_text(
        contents=[text], target_language_code=target_language_code, parent=parent
    )
    return response.translations[0].translated_text if response.translations else ""
