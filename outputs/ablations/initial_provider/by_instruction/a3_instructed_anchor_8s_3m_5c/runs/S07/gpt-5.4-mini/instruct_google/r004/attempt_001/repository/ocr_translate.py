import os

from google.cloud import translate_v3 as translate


def translate_ocr_text(text: str, target_language: str = "en") -> str:
    client = translate.TranslationServiceClient()
    project_id = os.getenv("GOOGLE_CLOUD_PROJECT")
    location = os.getenv("GOOGLE_CLOUD_LOCATION", "global")
    parent = f"projects/{project_id}/locations/{location}"
    response = client.translate_text(contents=[text], target_language_code=target_language, parent=parent)
    return response.translations[0].translated_text
