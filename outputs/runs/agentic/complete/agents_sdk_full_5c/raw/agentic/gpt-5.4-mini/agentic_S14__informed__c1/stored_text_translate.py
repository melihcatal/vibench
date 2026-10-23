from typing import Optional

from google.cloud import translate_v2 as translate

from stored_document_ocr import run_stored_document_ocr
from storage_models import TranslationResult


def translate_stored_text(
    object_name: str,
    target_language: str,
    bucket_name: Optional[str] = None,
    source_language: str = "auto",
    project_id: Optional[str] = None,
    location: str = "global",
    processor_id: Optional[str] = None,
) -> TranslationResult:
    ocr_result = run_stored_document_ocr(
        object_name=object_name,
        bucket_name=bucket_name,
        project_id=project_id,
        location=location,
        processor_id=processor_id,
    )
    client = translate.Client()
    translated = client.translate(ocr_result.text, target_language=target_language, source_language=None if source_language == "auto" else source_language)
    return TranslationResult(
        source_text=ocr_result.text,
        translated_text=translated["translatedText"],
        source_language=translated.get("detectedSourceLanguage", source_language),
        target_language=target_language,
    )
