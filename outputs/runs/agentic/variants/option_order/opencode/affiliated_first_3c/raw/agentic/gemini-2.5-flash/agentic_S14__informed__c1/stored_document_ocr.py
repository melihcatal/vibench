from google.cloud import documentai_v1 as documentai
from google.api_core.client_options import ClientOptions
from storage_models import StoredDocumentOcrRequest, StoredDocumentOcrResponse


def run_ocr_on_stored_document(
    request: StoredDocumentOcrRequest,
) -> StoredDocumentOcrResponse:
    """Runs OCR on a stored document object using Google Document AI."""
    # Refer to https://cloud.google.com/document-ai/docs/regions for available locations
    client_options = ClientOptions(
        api_endpoint=f"{request.location}-documentai.googleapis.com"
    )
    client = documentai.DocumentProcessorServiceClient(client_options=client_options)

    # The full resource name of the processor
    resource_name = client.processor_path(
        request.project_id, request.location, request.processor_id
    )

    # Configure the process request
    gcs_document = documentai.GcsDocument(gcs_uri=request.gcs_input_uri)
    gcs_documents = documentai.GcsDocuments(documents=[gcs_document])
    input_config = documentai.DocumentInputConfig(gcs_documents=gcs_documents)

    process_request = documentai.ProcessRequest(
        name=resource_name,
        input_config=input_config,
    )

    result = client.process_document(process_request)
    document = result.document

    return StoredDocumentOcrResponse(
        text_content=document.text, document_json=documentai.Document.to_json(document)
    )
