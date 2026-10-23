import os
from typing import Dict, Any
from google.api_core.client_options import ClientOptions
from google.cloud import documentai


def extract_invoice_fields(file_path: str, mime_type: str) -> Dict[str, Any]:
    """
    Extracts structured fields from an invoice using Google Document AI.
    """
    project_id = os.getenv("GOOGLE_CLOUD_PROJECT")
    location = "us"
    processor_id = "invoice-processor"

    if not project_id:
        raise ValueError("Google Cloud project ID must be set as GOOGLE_CLOUD_PROJECT")

    opts = ClientOptions(api_endpoint=f"{location}-documentai.googleapis.com")
    client = documentai.DocumentProcessorServiceClient(client_options=opts)

    name = client.processor_path(project_id, location, processor_id)

    with open(file_path, "rb") as image:
        image_content = image.read()

    raw_document = documentai.RawDocument(content=image_content, mime_type=mime_type)

    request = documentai.ProcessRequest(name=name, raw_document=raw_document)
    result = client.process_document(request=request)
    document = result.document

    extracted_fields = {}
    if document.entities:
        for entity in document.entities:
            field_name = entity.type_
            field_value = entity.mention_text
            confidence = entity.confidence
            extracted_fields[field_name] = {
                "value": field_value,
                "confidence": confidence,
            }

    return extracted_fields
