from __future__ import annotations

from typing import Optional

from google.cloud import documentai

from storage_client import get_bucket
from storage_models import NormalizedText


def run_stored_document_ocr(
    bucket_name: str,
    object_name: str,
    project_id: str,
    location: str,
    processor_id: str,
) -> NormalizedText:
    bucket = get_bucket(bucket_name)
    blob = bucket.blob(object_name)
    content = blob.download_as_bytes()

    client = documentai.DocumentProcessorServiceClient()
    name = client.processor_path(project_id, location, processor_id)
    raw_document = documentai.RawDocument(content=content, mime_type=blob.content_type or "application/pdf")
    request = documentai.ProcessRequest(name=name, raw_document=raw_document)
    result = client.process_document(request=request)
    text = result.document.text or ""
    return NormalizedText(text=text, source="google-document-ai")
