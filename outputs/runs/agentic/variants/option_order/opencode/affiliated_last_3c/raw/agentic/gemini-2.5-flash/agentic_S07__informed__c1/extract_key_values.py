import os
from google.cloud import documentai_v1 as documentai
from document_client import get_documentai_client


def extract_key_values_from_document(
    project_id: str,
    location: str,
    processor_id: str,
    file_content: bytes,
    mime_type: str,
):
    """Extracts key-value pairs from a form-like document using Google Document AI."""
    client = get_documentai_client()
    processor_name = client.processor_path(project_id, location, processor_id)

    raw_document = documentai.RawDocument(content=file_content, mime_type=mime_type)
    request = documentai.ProcessRequest(name=processor_name, raw_document=raw_document)

    response = client.process_document(request=request)
    document = response.document

    key_value_pairs = {}
    for entity in document.entities:
        if entity.type == "form_field":
            key = documentai.text_anchor_to_text(entity.text_anchor, document.text)
            value = (
                documentai.text_anchor_to_text(
                    entity.normalized_value.text_anchor, document.text
                )
                if entity.normalized_value
                else ""
            )
            key_value_pairs[key] = value

    # Also check from page.form_fields
    for page in document.pages:
        for field in page.form_fields:
            key = documentai.text_anchor_to_text(
                field.field_name.text_anchor, document.text
            )
            value = documentai.text_anchor_to_text(
                field.field_value.text_anchor, document.text
            )
            key_value_pairs[key] = value

    return key_value_pairs
