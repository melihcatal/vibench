import os
from google.cloud import documentai_v1 as documentai
from document_client import get_documentai_client
from document_models import FieldExtractionRequest, FieldExtractionResponse


def extract_structured_fields(
    request: FieldExtractionRequest,
) -> FieldExtractionResponse:
    """Extracts structured fields from OCR-normalized document text using Google Document AI's Invoice Parser."""
    client = get_documentai_client()
    processor_name = client.processor_path(
        request.project_id, request.location, request.processor_id
    )  # Example: "invoice-parser"

    raw_document = documentai.RawDocument(
        content=request.file_content, mime_type=request.mime_type
    )
    process_request = documentai.ProcessRequest(
        name=processor_name, raw_document=raw_document
    )

    response = client.process_document(request=process_request)
    document = response.document

    extracted_fields = {}
    for entity in document.entities:
        # Document AI entities have a type_ for identifying the field
        # and typically a mention_text or normalized_value for the content
        entity_value = documentai.text_anchor_to_text(entity.text_anchor, document.text)
        if entity.normalized_value:
            entity_value = (
                entity.normalized_value.text
                or entity.normalized_value.date_value
                or entity.normalized_value.money_value
                or entity.normalized_value.datetime_value
            )

        extracted_fields[entity.type_] = entity_value

    return FieldExtractionResponse(fields=extracted_fields)
