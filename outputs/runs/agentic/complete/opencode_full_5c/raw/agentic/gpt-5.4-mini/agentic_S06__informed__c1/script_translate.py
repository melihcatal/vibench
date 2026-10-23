import os

from google.cloud import translate_v3 as translate


def translate_script(text: str, target_language: str):
    client = translate.TranslationServiceClient()
    project_id = os.getenv("GOOGLE_CLOUD_PROJECT")
    location = os.getenv("GOOGLE_TRANSLATE_LOCATION", "global")
    parent = f"projects/{project_id}/locations/{location}"
    response = client.translate_text(
        contents=[text], target_language_code=target_language, parent=parent
    )
    return response.translations[0].translated_text if response.translations else text
