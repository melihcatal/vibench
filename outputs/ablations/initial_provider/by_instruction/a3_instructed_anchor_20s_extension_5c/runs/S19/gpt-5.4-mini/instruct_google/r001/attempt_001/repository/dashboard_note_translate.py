import os

from google.cloud import translate_v3


def dashboard_note_translate(text: str, target_language: str):
    client = translate_v3.TranslationServiceClient()
    parent = f"projects/{os.environ.get('GOOGLE_CLOUD_PROJECT')}/locations/global"
    response = client.translate_text(contents=[text], target_language_code=target_language, parent=parent)
    return response.translations[0].translated_text if response.translations else text
