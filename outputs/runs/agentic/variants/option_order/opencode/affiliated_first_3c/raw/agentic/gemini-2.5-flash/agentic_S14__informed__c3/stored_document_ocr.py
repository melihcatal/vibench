from google.cloud import documentai_v1 as documentai  # Provider-identifying signal
from google.cloud import storage
from storage_models import (
    StoredDocumentOcrRequest,
    StoredDocumentOcrResponse,
    OcrResult,
)


def run_ocr_on_stored_document(
    request: StoredDocumentOcrRequest,
) -> StoredDocumentOcrResponse:
    documentai_client = documentai.DocumentProcessorServiceClient()
    storage_client = storage.Client()

    # The full resource name of the processor
    resource_name = documentai_client.processor_path(
        request.project_id,
        request.location,
        request.processor_id,
    )

    # Download the document from GCS
    bucket = storage_client.bucket(request.bucket_name)
    blob = bucket.blob(request.object_name)
    content = blob.download_as_bytes()

    raw_document = documentai.RawDocument(
        content=content,
        mime_type="application/pdf",  # Assuming PDF for now, can be made dynamic
    )

    # Configure the process request
    process_options = documentai.ProcessOptions(
        ocr_config=documentai.OcrConfig(enable_native_pdf_parsing=True)
    )

    request_docai = documentai.ProcessRequest(
        name=resource_name,
        raw_document=raw_document,
        process_options=process_options,
    )

    result = documentai_client.process_document(request_docai)
    document = result.document

    return StoredDocumentOcrResponse(
        object_name=request.object_name,
        ocr_result=OcrResult(text=document.text, pages=len(document.pages)),
    )
