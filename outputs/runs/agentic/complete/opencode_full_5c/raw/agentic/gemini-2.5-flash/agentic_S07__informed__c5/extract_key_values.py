from google.cloud import documentai_v1beta3 as documentai
import os
from document_client import get_documentai_client


def extract_key_values_from_document(
    project_id: str, location: str, processor_id: str, file_path: str
):
    """
    Extracts key-value pairs from a form-like document using Google Document AI.
    """
    client = get_documentai_client()

    name = client.processor_path(project_id, location, processor_id)

    with open(file_path, "rb") as image:
        image_content = image.read()

    raw_document = documentai.RawDocument(
        content=image_content, mime_type="application/pdf"
    )

    request = documentai.ProcessRequest(name=name, raw_document=raw_document)
    result = client.process_document(request=request)
    document = result.document

    key_value_pairs = []
    for page in document.pages:
        for form_field in page.form_fields:
            key = page.get_text(form_field.field_name.text_anchor)
            value = page.get_text(form_field.field_value.text_anchor)
            key_value_pairs.append({"key": key, "value": value})

    return key_value_pairs
