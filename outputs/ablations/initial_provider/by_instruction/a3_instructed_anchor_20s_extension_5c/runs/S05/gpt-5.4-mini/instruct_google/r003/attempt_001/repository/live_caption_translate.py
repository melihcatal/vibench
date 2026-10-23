import os

from google.cloud import translate_v3 as translate

from speech_models import normalize_text


def translate_live_caption(text: str, target_language: str = "es") -> str:
    client = translate.TranslationServiceClient()
    parent = f"projects/{os.getenv('GOOGLE_CLOUD_PROJECT')}/locations/global"
    response = client.translate_text(
        request={
            "parent": parent,
            "contents": [normalize_text(text)],
            "mime_type": "text/plain",
            "target_language_code": target_language,
        }
    )
    return response.translations[0].translated_text if response.translations else ""
