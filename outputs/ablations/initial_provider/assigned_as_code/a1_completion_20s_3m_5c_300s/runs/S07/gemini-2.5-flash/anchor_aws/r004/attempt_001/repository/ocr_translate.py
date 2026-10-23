import os
from typing import Dict, Any
from google.cloud import translate_v3 as translate
from document_client import DocumentClient
from document_models import TranslationResult

def ocr_translate(text: str, target_language: str, source_language: str = None, config: Dict[str, Any] = None) -> TranslationResult:
    config = config or {}
    client = DocumentClient(config).get_translation_client()
    project_id = config.get("gcp_project_id", os.environ.get("GCP_PROJECT_ID"))

    if not project_id:
        raise ValueError("GCP_PROJECT_ID not found in config or environment variables.")

    parent = f"projects/{project_id}/locations/global"

    response = client.translate_text(
        request={
            "parent": parent,
            "contents": [text],
            "target_language_code": target_language,
            "source_language_code": source_language if source_language else None,
        }
    )

    translated_text = ""
    detected_source_language = source_language

    for translation in response.translations:
        translated_text += translation.translated_text
        if not detected_source_language and translation.detected_language_code:
            detected_source_language = translation.detected_language_code

    return TranslationResult(
        translated_text=translated_text,
        target_language=target_language,
        source_language=detected_source_language
    )
