import os
from google.cloud import translate_v3 as translate

GOOGLE_APPLICATION_CREDENTIALS = os.environ.get("GOOGLE_APPLICATION_CREDENTIALS")
PROJECT_ID = os.environ.get("GOOGLE_CLOUD_PROJECT")


def translate_appeal_text(text: str, target_language: str = "en"):
    client = translate.TranslationServiceClient()
    parent = f"projects/{PROJECT_ID}"
    response = client.translate_text(
        request={
            "parent": parent,
            "contents": [text],
            "target_language_code": target_language,
        }
    )
    if response.translations:
        return response.translations[0].translated_text
    return text
