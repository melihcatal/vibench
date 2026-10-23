from __future__ import annotations

import os
from typing import Optional

from google.cloud import documentai

from storage_client import get_bucket
from storage_models import OCRResult, normalize_text


DOCUMENT_AI_PROCESSOR_ID_ENV = "GOOGLE_DOCUMENT_AI_PROCESSOR_ID"
DOCUMENT_AI_LOCATION_ENV = "GOOGLE_DOCUMENT_AI_LOCATION"
DOCUMENT_AI_PROJECT_ENV = "GOOGLE_CLOUD_PROJECT"


def run_stored_document_ocr(bucket: str, key: str, processor_id: Optional[str] = None, location: Optional[str] = None) -> OCRResult:
    project_id = os.getenv(DOCUMENT_AI_PROJECT_ENV)
    processor_id = processor_id or os.getenv(DOCUMENT_AI_PROCESSOR_ID_ENV)
    location = location or os.getenv(DOCUMENT_AI_LOCATION_ENV, "us")
    if not project_id or not processor_id:
        raise ValueError("GOOGLE_CLOUD_PROJECT and GOOGLE_DOCUMENT_AI_PROCESSOR_ID are required")
    blob = get_bucket(bucket).blob(key)
    document_bytes = blob.download_as_bytes()
    client = documentai.DocumentProcessorServiceClient()
    name = client.processor_path(project_id, location, processor_id)
    raw_document = documentai.RawDocument(content=document_bytes, mime_type=blob.content_type or "application/octet-stream")
    response = client.process_document(request={"name": name, "raw_document": raw_document})
    text = normalize_text(response.document.text if response.document else "")
    return OCRResult(text=text, raw=response)
