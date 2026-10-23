import os
from google.cloud import translate_v3 as translate
from vision_client import GOOGLE_CLOUD_PROJECT


def alt_text_translate(text: str, target_language: str = "es") -> str:
    client = translate.TranslationServiceClient()
    if not GOOGLE_CLOUD_PROJECT:
        raise ValueError("GOOGLE_CLOUD_PROJECT env var required")
    parent = f"projects/{GOOGLE_CLOUD_PROJECT}"
    response = client.translate_text(
        request={
            "parent": parent,
            "contents": [text],
            "mime_type": "text/plain",
            "source_language_code": "en",
            "target_language_code": target_language,
        }
    )
    return response.translations[0].translated_text
