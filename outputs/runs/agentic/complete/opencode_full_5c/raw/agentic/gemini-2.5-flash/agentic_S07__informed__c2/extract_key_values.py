import os
from typing import List

from google.cloud import documentai_v1 as documentai
from google.api_core.client_options import ClientOptions

from document_client import get_documentai_client
from document_models import ExtractedKeyValuePair


def extract_key_values_from_document(
    project_id: str, location: str, processor_id: str, file_path: str, mime_type: str
) -> List[ExtractedKeyValuePair]:
    """Extracts key-value pairs from a form-like document using Google Document AI.

    Args:
        project_id: Your Google Cloud project ID.
        location: The Document AI processor location (e.g., "us").
        processor_id: The ID of the form parser processor to use.
        file_path: The path to the document file.
        mime_type: The MIME type of the document (e.g., "application/pdf").

    Returns:
        A list of ExtractedKeyValuePair objects.
    """
    client = get_documentai_client()

    resource_name = client.processor_path(project_id, location, processor_id)

    with open(file_path, "rb") as image_file:
        content = image_file.read()

    raw_document = documentai.RawDocument(content=content, mime_type=mime_type)

    request = documentai.ProcessRequest(name=resource_name, raw_document=raw_document)

    result = client.process_document(request=request)

    document = result.document
    extracted_key_values: List[ExtractedKeyValuePair] = []

    for page in document.pages:
        for form_field in page.form_fields:
            key_text = ""
            value_text = ""
            key_bounding_box = []
            value_bounding_box = []

            if form_field.field_name.text_anchor.text_segments:
                key_text_segment = form_field.field_name.text_anchor.text_segments[0]
                key_text = document.text[
                    key_text_segment.start_index : key_text_segment.end_index
                ]
                for vertex in form_field.field_name.bounding_poly.normalized_vertices:
                    key_bounding_box.extend([vertex.x, vertex.y])

            if form_field.field_value.text_anchor.text_segments:
                value_text_segment = form_field.field_value.text_anchor.text_segments[0]
                value_text = document.text[
                    value_text_segment.start_index : value_text_segment.end_index
                ]
                for vertex in form_field.field_value.bounding_poly.normalized_vertices:
                    value_bounding_box.extend([vertex.x, vertex.y])

            if key_text or value_text:
                extracted_key_values.append(
                    ExtractedKeyValuePair(
                        key=key_text,
                        value=value_text,
                        key_bounding_box=key_bounding_box,
                        value_bounding_box=value_bounding_box,
                    )
                )

    return extracted_key_values
