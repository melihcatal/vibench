import os
from typing import Union

from google.cloud import documentai_v1 as documentai

from document_client import GoogleCloudClients
from document_models import ExtractedKeyValues, KeyValuePair, BoundingPoly


def _convert_bounding_poly(document_proto_bounding_poly) -> BoundingPoly:
    if not document_proto_bounding_poly:
        return BoundingPoly(vertices=[])
    vertices = []
    for vertex in document_proto_bounding_poly.vertices:
        vertices.append({"x": vertex.x, "y": vertex.y})
    return BoundingPoly(vertices=vertices)


def extract_key_values_from_document(
    document_bytes: bytes, mime_type: str
) -> ExtractedKeyValues:
    """Extracts key-value pairs from a form-like document using Google Cloud Document AI.

    Args:
        document_bytes: The content of the document file as bytes.
        mime_type: The MIME type of the document (e.g., 'application/pdf', 'image/tiff').

    Returns:
        An ExtractedKeyValues object containing a list of key-value pairs.
    """
    project_id = os.environ.get("GOOGLE_PROJECT_ID")
    location = os.environ.get("GOOGLE_LOCATION")
    # Using a general form parser processor for key-value extraction
    processor_id = os.environ.get(
        "DOCUMENT_AI_PROCESSOR_ID", "YOUR_FORM_PARSER_PROCESSOR_ID"
    )  # Replace with your processor ID

    if not project_id or not location or not processor_id:
        raise ValueError(
            "GOOGLE_PROJECT_ID, GOOGLE_LOCATION, and DOCUMENT_AI_PROCESSOR_ID environment variables must be set."
        )

    client = GoogleCloudClients.get_documentai_client()

    name = client.processor_path(project_id, location, processor_id)

    raw_document = documentai.RawDocument(content=document_bytes, mime_type=mime_type)

    request = documentai.ProcessRequest(name=name, raw_document=raw_document)

    response = client.process_document(request=request)
    document = response.document

    key_value_pairs: list[KeyValuePair] = []

    for page in document.pages:
        for form_field in page.form_fields:
            key_text = document.text[
                form_field.field_name.text_anchor.text_segments[
                    0
                ].start_index : form_field.field_name.text_anchor.text_segments[
                    0
                ].end_index
            ]
            value_text = document.text[
                form_field.field_value.text_anchor.text_segments[
                    0
                ].start_index : form_field.field_value.text_anchor.text_segments[
                    0
                ].end_index
            ]

            key_value_pairs.append(
                KeyValuePair(
                    key=key_text,
                    value=value_text,
                    key_bounding_box=_convert_bounding_poly(
                        form_field.field_name.bounding_poly
                    ),
                    value_bounding_box=_convert_bounding_poly(
                        form_field.field_value.bounding_poly
                    ),
                )
            )
    return ExtractedKeyValues(key_value_pairs=key_value_pairs)
