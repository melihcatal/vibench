from __future__ import annotations

from typing import List

from google.cloud import translate_v3 as translate

from document_models import NormalizedDocumentText, normalize_text

PROVIDER = "google-cloud-translate"
MODEL_ID = "translate-text-v3"


def ocr_translate(text: str, target_language_code: str, parent: str) -> str:
    client = translate.TranslationServiceClient()
    response = client.translate_text(
        request={
            "parent": parent,
            "contents": [normalize_text(text).text],
            "target_language_code": target_language_code,
            "mime_type": "text/plain",
        }
    )
    translations: List[str] = [item.translated_text for item in response.translations]
    return "\n".join(translations)
