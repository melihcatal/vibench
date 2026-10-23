import os

from google.cloud import translate_v3


def payload_translate(text: str, target_language: str = "es"):
    client = translate_v3.TranslationServiceClient()
    parent = f"projects/{os.getenv('GOOGLE_CLOUD_PROJECT')}/locations/global"
    response = client.translate_text(
        contents=[text], target_language_code=target_language, parent=parent
    )
    translated = (
        response.translations[0].translated_text if response.translations else text
    )
    return {"translated_text": translated, "provider": "google-cloud-translate"}
