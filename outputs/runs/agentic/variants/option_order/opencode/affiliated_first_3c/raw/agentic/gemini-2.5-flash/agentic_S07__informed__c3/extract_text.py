import os
from document_client import DocumentClient
from document_models import DocumentExtractionRequest, DocumentExtractionResponse
from google.cloud import documentai_v1 as documentai


def extract_plain_text(
    request: DocumentExtractionRequest,
) -> DocumentExtractionResponse:
    client_helper = DocumentClient()
    client = client_helper.get_documentai_client()
    project_id = client_helper.project_id
    location = client_helper.location
    processor_id = os.getenv(
        "DOCUMENTAI_TEXT_PROCESSOR_ID"
    )  # e.g., "YOUR_TEXT_PROCESSOR_ID"

    if not project_id or not processor_id:
        raise ValueError(
            "GOOGLE_CLOUD_PROJECT_ID and DOCUMENTAI_TEXT_PROCESSOR_ID environment variables must be set."
        )

    name = client.processor_path(project_id, location, processor_id)

    raw_document = documentai.RawDocument(
        content=request.content,
        mime_type=request.mime_type,
    )

    request_obj = documentai.ProcessRequest(name=name, raw_document=raw_document)
    result = client.process_document(request=request_obj)

    document_text = result.document.text
    return DocumentExtractionResponse(text=document_text, document_obj=result.document)
