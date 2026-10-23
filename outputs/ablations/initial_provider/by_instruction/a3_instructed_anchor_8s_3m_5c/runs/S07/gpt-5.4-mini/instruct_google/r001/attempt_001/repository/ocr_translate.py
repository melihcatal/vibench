import os

from google.cloud import translate_v3

from document_models import normalize_text


def translate_ocr_text(text: str, target_language: str) -> str:
    client = translate_v3.TranslationServiceClient()
    project = os.getenv("GOOGLE_CLOUD_PROJECT") or os.getenv("GCP_PROJECT")
    parent = f"projects/{project}/locations/global"
    response = client.translate_text(
        request={
            "parent": parent,
            "contents": [normalize_text(text)],
            "mime_type": "text/plain",
            "target_language_code": target_language,
        }
    )
    return normalize_text(response.translations[0].translated_text if response.translations else text)
