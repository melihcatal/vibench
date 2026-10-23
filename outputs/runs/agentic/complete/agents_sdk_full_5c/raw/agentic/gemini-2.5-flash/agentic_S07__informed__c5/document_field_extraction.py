import os
from google.cloud import documentai_v1beta3 as documentai
from document_client import get_documentai_client
from document_models import DocumentFieldExtractionRequest, DocumentFieldExtractionResponse

def extract_structured_fields(request: DocumentFieldExtractionRequest) -> DocumentFieldExtractionResponse:
    """Extracts structured fields from OCR-normalized document text using Google Document AI Invoice Parser."""
    client = get_documentai_client()
    # The processor_id from the request is used here, which should be for a specific prebuilt processor like 'invoice-parser'
    processor_name = client.processor_path(
        os.environ.get("GOOGLE_CLOUD_PROJECT"),
        os.environ.get("GOOGLE_CLOUD_LOCATION"),
        request.processor_id
    )

    with open(request.document_path, "rb") as image:
        image_content = image.read()

    raw_document = documentai.RawDocument(
        content=image_content,
        mime_type=request.mime_type
    )

    request_docai = documentai.ProcessRequest(
        name=processor_name,
        raw_document=raw_document
    )

    result = client.process_document(request_docai)
    document = result.document

    extracted_fields = {}
    # Extract fields based on the processor's output
    # For an Invoice Parser, you'd typically look for entities
    for entity in document.entities:
        # Entities often have properties like type, mention_text, and normalized_value
        # Adjust this logic based on the specific output structure of the Invoice Parser
        field_name = entity.type_ or "untyped_field"
        field_value = entity.mention_text or ""
        if entity.normalized_value and entity.normalized_value.text:
            field_value = entity.normalized_value.text
        
        if field_name not in extracted_fields:
            extracted_fields[field_name] = []
        extracted_fields[field_name].append(field_value)

    return DocumentFieldExtractionResponse(
        extracted_fields=extracted_fields
    )
