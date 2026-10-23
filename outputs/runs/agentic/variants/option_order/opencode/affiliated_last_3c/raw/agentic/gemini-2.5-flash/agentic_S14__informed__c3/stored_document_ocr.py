from google.cloud import documentai_v1beta3 as documentai
from google.api_core.client_options import ClientOptions
from storage_models import StoredDocumentOcrRequest, StoredDocumentOcrResponse


def run_ocr_on_stored_document(
    request: StoredDocumentOcrRequest,
) -> StoredDocumentOcrResponse:
    """Runs OCR on a stored document object using Google Document AI."""
    # Google Document AI setup
    location = "us"  # e.g., "us" or "eu"
    project_id = os.environ.get("GOOGLE_CLOUD_PROJECT")
    if not project_id:
        raise ValueError("GOOGLE_CLOUD_PROJECT environment variable not set.")

    processor_id = os.environ.get("GOOGLE_DOCUMENT_AI_PROCESSOR_ID")
    if not processor_id:
        raise ValueError(
            "GOOGLE_DOCUMENT_AI_PROCESSOR_ID environment variable not set."
        )

    # The full resource name of the processor
    # e.g.: projects/project_id/locations/location/processors/processor_id
    processor_name = (
        f"projects/{project_id}/locations/{location}/processors/{processor_id}"
    )

    client_options = ClientOptions(api_endpoint=f"{location}-documentai.googleapis.com")
    client = documentai.DocumentProcessorServiceClient(client_options=client_options)

    # The GCS URI to the document, e.g. gs://the-document-bucket/document.pdf
    gcs_document_uri = f"gs://{request.bucket_name}/{request.object_name}"

    # Refer to https://cloud.google.com/document-ai/docs/file-types for supported file types
    raw_document = documentai.RawDocument(gcs_uri=gcs_document_uri)

    # Configure the process request
    process_options = documentai.ProcessOptions(
        # Set to OCR_WITH_NATIVE_TEXT if you want to use the native text
        ocr_config=documentai.OcrConfig(enable_native_pdf_text=True)
    )
    document_request = documentai.ProcessRequest(
        name=processor_name,
        raw_document=raw_document,
        process_options=process_options,
    )

    result = client.process_document(document_request)
    document = result.document

    text_content = document.text
    page_count = len(document.pages)

    return StoredDocumentOcrResponse(text_content=text_content, page_count=page_count)
