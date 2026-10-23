from __future__ import annotations

from google.cloud import documentai_v1 as documentai

from storage_client import get_google_project_id
from storage_models import StoredDocumentOcrRequest, StoredDocumentOcrResponse


def run_stored_document_ocr(
    request: StoredDocumentOcrRequest,
) -> StoredDocumentOcrResponse:
    project_id = get_google_project_id()
    location = "us"
    processor_id = "ocr"
    client = documentai.DocumentProcessorServiceClient()
    name = client.processor_path(project_id, location, processor_id)
    gcs_uri = f"gs://{request.bucket}/{request.object_key}"
    raw_document = documentai.RawDocument(content=b"", mime_type="application/pdf")
    gcs_document = documentai.GcsDocument(gcs_uri=gcs_uri, mime_type="application/pdf")
    gcs_documents = documentai.GcsDocuments(documents=[gcs_document])
    batch_input_config = documentai.BatchDocumentsInputConfig(
        gcs_documents=gcs_documents
    )
    process_request = documentai.ProcessRequest(
        name=name,
        inline_document=documentai.Document(
            content=raw_document.content, mime_type=raw_document.mime_type
        ),
    )
    result = client.process_document(request=process_request)
    document = result.document
    pages = [
        {
            "page_number": page.page_number,
            "dimension": {
                "width": page.dimension.width,
                "height": page.dimension.height,
            },
        }
        for page in document.pages
    ]
    return StoredDocumentOcrResponse(
        bucket=request.bucket,
        object_key=request.object_key,
        provider="google_document_ai",
        extracted_text=document.text or "",
        pages=pages,
    )
