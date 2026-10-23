from google.cloud import documentai_v1beta3 as documentai
import os
from document_client import get_documentai_client


def extract_invoice_fields(
    project_id: str, location: str, processor_id: str, file_path: str
) -> dict:
    """
    Extracts structured fields from an invoice document using Google Document AI Invoice Parser.
    """
    client = get_documentai_client()

    # The full resource name of the processor
    # e.g., projects/project_id/locations/location/processors/processor_id
    name = client.processor_path(project_id, location, processor_id)

    with open(file_path, "rb") as image:
        image_content = image.read()

    raw_document = documentai.RawDocument(
        content=image_content, mime_type="application/pdf"
    )  # Assuming PDF for invoices

    request = documentai.ProcessRequest(name=name, raw_document=raw_document)
    result = client.process_document(request=request)
    document = result.document

    extracted_fields = {}
    for entity in document.entities:
        # Accessing normalized value or text for simplicity
        if entity.normalized_value and entity.normalized_value.text:
            value = entity.normalized_value.text
        elif entity.text_anchor and entity.text_anchor.text_segments:
            value = document.get_text(entity.text_anchor)
        else:
            value = entity.mention_text

        extracted_fields[entity.type_] = value

    return extracted_fields
