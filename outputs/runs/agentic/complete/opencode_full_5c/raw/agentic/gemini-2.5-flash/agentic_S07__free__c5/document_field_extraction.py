import os
from google.cloud import documentai_v1 as documentai
from document_client import get_documentai_client
from document_models import FieldExtractionResponse


def extract_structured_fields_from_document(
    file_content: bytes, mime_type: str
) -> FieldExtractionResponse:
    project_id = os.environ.get("GOOGLE_CLOUD_PROJECT")
    location = os.environ.get("GOOGLE_CLOUD_LOCATION", "us")  # e.g., "us"
    processor_id = os.environ.get(
        "GOOGLE_CLOUD_DOCUMENTAI_PROCESSOR_ID_INVOICE", "INVOICE_PROCESSOR_ID_HERE"
    )  # Replace with your Invoice Processor ID

    if not project_id:
        raise ValueError("GOOGLE_CLOUD_PROJECT environment variable not set.")

    client = get_documentai_client()

    resource_name = client.processor_path(project_id, location, processor_id)

    document = documentai.RawDocument(content=file_content, mime_type=mime_type)

    request = documentai.ProcessRequest(name=resource_name, raw_document=document)

    result = client.process_document(request=request)
    document_response = result.document

    extracted_fields = {}
    for entity in document_response.entities:
        # For specialized processors, entities often represent the structured fields
        if entity.type_ and entity.mention_text:
            extracted_fields[entity.type_] = documentai.get_text_anchor_text(
                entity.text_anchor, document_response.text
            )
            # You might need more sophisticated logic to handle complex entity structures
            # e.g., if an entity has multiple properties or child entities

    return FieldExtractionResponse(fields=extracted_fields)
