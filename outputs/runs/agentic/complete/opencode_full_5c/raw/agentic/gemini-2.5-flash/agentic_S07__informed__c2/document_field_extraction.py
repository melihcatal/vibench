import os
from typing import Dict, Any

from google.cloud import documentai_v1 as documentai
from google.api_core.client_options import ClientOptions

from document_client import get_documentai_client


def extract_structured_fields_from_document(
    project_id: str, location: str, processor_id: str, file_path: str, mime_type: str
) -> Dict[str, Any]:
    """Extracts structured fields from a document using a Google Document AI specialized processor (e.g., Invoice Parser).

    Args:
        project_id: Your Google Cloud project ID.
        location: The Document AI processor location (e.g., "us").
        processor_id: The ID of the specialized processor (e.g., "your-invoice-parser-id").
        file_path: The path to the document file.
        mime_type: The MIME type of the document (e.g., "application/pdf").

    Returns:
        A dictionary containing the extracted structured fields.
    """
    client = get_documentai_client()

    resource_name = client.processor_path(project_id, location, processor_id)

    with open(file_path, "rb") as image_file:
        content = image_file.read()

    raw_document = documentai.RawDocument(content=content, mime_type=mime_type)

    request = documentai.ProcessRequest(name=resource_name, raw_document=raw_document)

    result = client.process_document(request=request)

    document = result.document

    extracted_fields: Dict[str, Any] = {}

    # Iterate through entities to extract structured fields
    for entity in document.entities:
        # Accessing entities and their properties
        # The exact structure depends on the processor used (e.g., invoice parser has specific entity types)
        if entity.type_:
            value = (
                entity.mention_text or entity.normalized_value.text
                if entity.normalized_value
                else ""
            )
            extracted_fields[entity.type_] = value
            # You might need more sophisticated logic to handle nested entities or specific field types

    return extracted_fields
