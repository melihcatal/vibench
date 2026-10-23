import os

from google.cloud import translate_v3 as translate

from identity_models import normalize_locale


def welcome_translate(text: str, locale: str = "en"):
    client = translate.TranslationServiceClient()
    project_id = os.getenv("GOOGLE_CLOUD_PROJECT", os.getenv("GCP_PROJECT", ""))
    parent = (
        f"projects/{project_id}/locations/global" if project_id else "locations/global"
    )
    response = client.translate_text(
        request={
            "parent": parent,
            "contents": [text],
            "mime_type": "text/plain",
            "target_language_code": normalize_locale(locale),
        }
    )
    return response.translations[0].translated_text if response.translations else text
