from google.cloud import documentai_v1 as documentai
from google.api_core.client_options import ClientOptions
from storage_models import StoredDocumentOcrRequest, StoredDocumentOcrResponse
import os

def run_ocr_on_stored_document(request: StoredDocumentOcrRequest) -> StoredDocumentOcrResponse:
    """Runs OCR on a stored document object using Google Document AI."""
    project_id = os.environ.get("GOOGLE_CLOUD_PROJECT") # Assumes GOOGLE_CLOUD_PROJECT env var is set
    location = "us"
    processor_id = os.environ.get("DOCUMENTAI_PROCESSOR_ID") # Specific processor ID for OCR

    if not project_id or not processor_id:
        raise ValueError("Environment variables GOOGLE_CLOUD_PROJECT and DOCUMENTAI_PROCESSOR_ID must be set.")

    opts = ClientOptions(api_endpoint=f"{location}-documentai.googleapis.com")
    client = documentai.DocumentProcessorServiceClient(client_options=opts)

    name = client.processor_path(project_id, location, processor_id)

    gcs_document = documentai.GcsDocument(
        gcs_uri=f"gs://{request.bucket_name}/{request.object_name}",
        mime_type=request.mime_type,
    )
    gcs_document_content = documentai.GcsDocumentContent(gcs_document=gcs_document)
    input_config = documentai.DocumentInputConfig(gcs_document_content=gcs_document_content)

    # Configure the process request
    process_request = documentai.ProcessRequest(name=name, input_config=input_config)

    # Use the Document AI client to process the document
    result = client.process_document(request=process_request)
    document = result.document

    return StoredDocumentOcrResponse(
        bucket_name=request.bucket_name,
        object_name=request.object_name,
        extracted_text=document.text,
        pages=[{'page_number': page.page_number, 'image_dimension': {'width': page.image.dimension.width, 'height': page.image.dimension.height}} for page in document.pages] if document.pages else []
    )
