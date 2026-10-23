from google.cloud import documentai_v1 as documentai

from document_client import documentai_client, documentai_raw_document, get_env, processor_name
from document_models import OCRRequest


def document_field_extraction(request: OCRRequest) -> dict:
    client = documentai_client()
    name = processor_name(get_env("GOOGLE_CLOUD_PROJECT", ""), get_env("GOOGLE_CLOUD_LOCATION", "us"), get_env("GOOGLE_CLOUD_DOCUMENTAI_FIELD_PROCESSOR_ID", ""))
    raw = documentai_raw_document(request.image_uri, request.image_bytes)
    result = client.process_document(name=name, raw_document=raw)
    return {"provider": "google_document_ai", "entities": [{"type": entity.type_, "value": entity.mention_text} for entity in result.document.entities]}
