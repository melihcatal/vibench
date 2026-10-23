import os
from typing import Optional

from google.cloud import translate_v3

from document_models import OCRResponse, TranslationResponse


TRANSLATION_PROJECT_ID = os.getenv("GOOGLE_CLOUD_PROJECT", os.getenv("GCP_PROJECT", ""))
TRANSLATION_LOCATION = os.getenv("TRANSLATE_LOCATION", "global")


def translate_ocr_text(ocr: OCRResponse, target_language_code: str, source_language_code: Optional[str] = None) -> TranslationResponse:
    client = translate_v3.TranslationServiceClient()
    parent = f"projects/{TRANSLATION_PROJECT_ID}/locations/{TRANSLATION_LOCATION}"
    response = client.translate_text(
        request={
            "parent": parent,
            "contents": [ocr.text],
            "mime_type": "text/plain",
            "target_language_code": target_language_code,
            "source_language_code": source_language_code or "",
        }
    )
    translated = response.translations[0].translated_text if response.translations else ""
    return TranslationResponse(translated_text=translated, raw=response)
