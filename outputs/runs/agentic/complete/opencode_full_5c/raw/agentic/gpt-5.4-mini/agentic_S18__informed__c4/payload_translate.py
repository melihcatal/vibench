import os

from google.cloud import translate_v3 as translate


def translate_payload(text, target_language):
    client = translate.TranslationServiceClient()
    parent = f"projects/{os.environ['GOOGLE_CLOUD_PROJECT']}/locations/global"
    response = client.translate_text(
        contents=[text], target_language_code=target_language, parent=parent
    )
    return response.translations[0].translated_text
