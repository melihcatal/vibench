import os
from google.cloud import documentai_v1beta3 as documentai
from google.api_core.client_options import ClientOptions
from document_models import (
    DocumentFieldExtractionRequest,
    DocumentFieldExtractionResult,
)


def extract_document_fields(
    request: DocumentFieldExtractionRequest,
) -> DocumentFieldExtractionResult:
    project_id = os.environ.get("GOOGLE_CLOUD_PROJECT_ID")
    location = "us"  # Processor location. For example, "us" or "eu"
    processor_id = os.environ.get(
        "DOCUMENT_AI_PROCESSOR_ID"
    )  # e.g., "YOUR_PROCESSOR_ID" for a custom processor or a prebuilt like "invoice-parser"

    if not project_id or not processor_id:
        raise ValueError(
            "GOOGLE_CLOUD_PROJECT_ID and DOCUMENT_AI_PROCESSOR_ID environment variables must be set."
        )

    # You must set the api_endpoint if your processor is not in the default global region
    client_options = ClientOptions(api_endpoint=f"{location}-documentai.googleapis.com")
    client = documentai.DocumentProcessorServiceClient(client_options=client_options)

    name = client.processor_path(project_id, location, processor_id)

    # Read the file into memory
    raw_document = documentai.RawDocument(
        content=request.document_content, mime_type=request.mime_type
    )

    # Configure the process request
    process_request = documentai.ProcessRequest(name=name, raw_document=raw_document)

    result = client.process_document(request=process_request)
    document = result.document

    extracted_fields = {}
    if document.entities:
        for entity in document.entities:
            # Recursively extract sub-entities if present
            def extract_entity_data(entity_obj):
                entity_data = {
                    "text_anchor": entity_obj.text_anchor.content
                    if entity_obj.text_anchor
                    else None,
                    "type": entity_obj.type_,
                    "mention_text": entity_obj.mention_text,
                    "confidence": entity_obj.confidence,
                }
                if entity_obj.properties:
                    entity_data["properties"] = {
                        prop.type_: extract_entity_data(prop)
                        for prop in entity_obj.properties
                    }
                return entity_data

            extracted_fields[entity.type_] = extract_entity_data(entity)

    return DocumentFieldExtractionResult(fields=extracted_fields)
