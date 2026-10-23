import os
from document_client import DocumentClient
from document_models import DocumentExtractionRequest, DocumentExtractionResponse
from google.cloud import documentai_v1 as documentai


def extract_structured_fields(
    request: DocumentExtractionRequest,
) -> DocumentExtractionResponse:
    client_helper = DocumentClient()
    client = client_helper.get_documentai_client()
    project_id = client_helper.project_id
    location = client_helper.location
    processor_id = os.getenv(
        "DOCUMENTAI_INVOICE_PROCESSOR_ID"
    )  # e.g., "YOUR_INVOICE_PROCESSOR_ID" for invoice parsing

    if not project_id or not processor_id:
        raise ValueError(
            "GOOGLE_CLOUD_PROJECT_ID and DOCUMENTAI_INVOICE_PROCESSOR_ID environment variables must be set."
        )

    name = client.processor_path(project_id, location, processor_id)

    raw_document = documentai.RawDocument(
        content=request.content,
        mime_type=request.mime_type,
    )

    request_obj = documentai.ProcessRequest(name=name, raw_document=raw_document)
    result = client.process_document(request=request_obj)

    extracted_fields = {}
    if result.document.entities:
        for entity in result.document.entities:
            # Document AI processors have predefined entity types (e.g., invoice fields)
            extracted_fields[entity.type_] = entity.mention_text

    return DocumentExtractionResponse(
        text=result.document.text,
        entities=extracted_fields,
        document_obj=result.document,
    )
