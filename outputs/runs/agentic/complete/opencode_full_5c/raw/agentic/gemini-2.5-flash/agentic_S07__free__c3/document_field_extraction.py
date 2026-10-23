import os
from typing import Union

from google.cloud import documentai_v1 as documentai

from document_client import GoogleCloudClients
from document_models import DocumentFieldExtractionResult, DocumentField, BoundingPoly


def _convert_bounding_poly(document_proto_bounding_poly) -> BoundingPoly:
    if not document_proto_bounding_poly:
        return BoundingPoly(vertices=[])
    vertices = []
    for vertex in document_proto_bounding_poly.vertices:
        vertices.append({"x": vertex.x, "y": vertex.y})
    return BoundingPoly(vertices=vertices)


def extract_structured_fields_from_document(
    document_bytes: bytes, mime_type: str
) -> DocumentFieldExtractionResult:
    """Extracts structured fields from OCR-normalized document using Google Cloud Document AI.

    Args:
        document_bytes: The content of the document file as bytes.
        mime_type: The MIME type of the document (e.g., 'application/pdf', 'image/tiff').

    Returns:
        A DocumentFieldExtractionResult object containing a list of extracted fields.
    """
    project_id = os.environ.get("GOOGLE_PROJECT_ID")
    location = os.environ.get("GOOGLE_LOCATION")
    # Using a general form parser processor for structured field extraction
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

    extracted_fields: list[DocumentField] = []

    for page in document.pages:
        for form_field in page.form_fields:
            field_name_text = document.text[
                form_field.field_name.text_anchor.text_segments[
                    0
                ].start_index : form_field.field_name.text_anchor.text_segments[
                    0
                ].end_index
            ]
            field_value_text = document.text[
                form_field.field_value.text_anchor.text_segments[
                    0
                ].start_index : form_field.field_value.text_anchor.text_segments[
                    0
                ].end_index
            ]

            extracted_fields.append(
                DocumentField(
                    field_name=field_name_text,
                    field_value=field_value_text,
                    field_bounding_box=_convert_bounding_poly(
                        form_field.field_name.bounding_poly
                    ),
                    value_bounding_box=_convert_bounding_poly(
                        form_field.field_value.bounding_poly
                    ),
                )
            )

    return DocumentFieldExtractionResult(fields=extracted_fields)
