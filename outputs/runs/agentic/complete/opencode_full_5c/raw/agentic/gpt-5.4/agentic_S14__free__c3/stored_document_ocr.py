from __future__ import annotations

from google.api_core.client_options import ClientOptions
from google.cloud import documentai_v1 as documentai

from storage_client import get_documentai_processor_name
from storage_models import OCRResult


def run_stored_document_ocr(bucket: str, key: str, mime_type: str) -> OCRResult:
    processor_name = get_documentai_processor_name()
    location = processor_name.split("/")[3]
    client = documentai.DocumentProcessorServiceClient(
        client_options=ClientOptions(
            api_endpoint=f"{location}-documentai.googleapis.com"
        )
    )
    gcs_uri = f"gs://{bucket}/{key}"
    request = documentai.ProcessRequest(
        name=processor_name,
        raw_document=None,
        gcs_document=documentai.GcsDocument(gcs_uri=gcs_uri, mime_type=mime_type),
        skip_human_review=True,
    )
    result = client.process_document(request=request)
    document = result.document
    pages = len(document.pages)
    return OCRResult(bucket=bucket, key=key, text=document.text or "", page_count=pages)
