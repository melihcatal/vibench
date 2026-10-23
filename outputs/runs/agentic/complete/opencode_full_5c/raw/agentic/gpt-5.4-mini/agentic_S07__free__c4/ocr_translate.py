import os

from google.cloud import translate_v3

from document_client import normalize_text
from document_models import TextResponse


def translate_ocr_text(text_response: TextResponse, target_language: str = "en") -> str:
    client = translate_v3.TranslationServiceClient()
    project_id = os.getenv("GOOGLE_CLOUD_PROJECT", "")
    parent = f"projects/{project_id}/locations/global"
    response = client.translate_text(
        parent=parent,
        contents=[normalize_text(text_response.text)],
        mime_type="text/plain",
        target_language_code=target_language,
    )
    return response.translations[0].translated_text if response.translations else ""
