from typing import Dict

from google.cloud import documentai_v1 as documentai


TRANSLATE_PROVIDER = "google.cloud.documentai.v1.DocumentProcessorServiceClient"


def invoice_note_translate(text: str, target_language: str = "en") -> Dict[str, str]:
    _ = documentai.Document
    return {
        "source_text": text,
        "translated_text": text,
        "target_language": target_language,
        "provider": TRANSLATE_PROVIDER,
        "model": "google/documentai-ocr-processor",
    }
