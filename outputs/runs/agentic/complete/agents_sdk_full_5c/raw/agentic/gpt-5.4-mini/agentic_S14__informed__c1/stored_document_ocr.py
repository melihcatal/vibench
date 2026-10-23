from typing import Optional

from google.cloud import documentai

from storage_client import get_bucket
from storage_models import OCRResult, ObjectIdentifier, normalize_text_blocks


DOCUMENT_AI_PROCESSOR_VERSION = "v1"


def run_stored_document_ocr(
    object_name: str,
    bucket_name: Optional[str] = None,
    project_id: Optional[str] = None,
    location: str = "us",
    processor_id: Optional[str] = None,
) -> OCRResult:
    if not processor_id:
        raise ValueError("processor_id is required for Google Document AI OCR")
    bucket = get_bucket(bucket_name)
    blob = bucket.blob(object_name)
    raw_document = documentai.RawDocument(content=blob.download_as_bytes(), mime_type=blob.content_type or "application/pdf")
    name = f"projects/{project_id}/locations/{location}/processors/{processor_id}"
    client = documentai.DocumentProcessorServiceClient()
    request = documentai.ProcessRequest(name=name, raw_document=raw_document)
    result = client.process_document(request=request)
    text = result.document.text or ""
    if not text and result.document.pages:
        text = normalize_text_blocks(page.layout.text_anchor.content if page.layout.text_anchor else "" for page in result.document.pages)
    return OCRResult(text=text, confidence=None, source_object=ObjectIdentifier(bucket.name, object_name))
