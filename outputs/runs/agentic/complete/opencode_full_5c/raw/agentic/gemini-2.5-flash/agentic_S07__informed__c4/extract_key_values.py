import os
from document_client import DocumentAIClient
from document_models import (
    DocumentResponse,
    DocumentPage,
    DocumentPageFormProperty,
    TextAnchor,
    TextSpan,
    BoundingPoly,
)
from google.cloud import documentai_v1 as documentai


def _get_text(
    document: documentai.Document, text_anchor: documentai.Document.TextAnchor
) -> str:
    """Helper to extract text from a text anchor."""
    if not text_anchor.text_segments:
        return ""

    full_text = ""
    for segment in text_anchor.text_segments:
        start_index = int(segment.start_index)
        end_index = int(segment.end_index)
        full_text += document.text[start_index:end_index]
    return full_text


def extract_document_key_values(
    file_content: bytes, mime_type: str, processor_id: str
) -> DocumentResponse:
    """
    Extracts key-value pairs from a form-like document using Google Document AI.
    """
    client = DocumentAIClient()
    document = client.process_document(file_content, mime_type, processor_id)

    pages_data = []
    for page in document.pages:
        form_fields_data = []
        for form_field in page.form_fields:
            key_text_anchor = TextAnchor(
                text_segments=[
                    TextSpan(
                        offset=int(ts.start_index),
                        length=int(ts.end_index) - int(ts.start_index),
                    )
                    for ts in form_field.field_name.text_anchor.text_segments
                ]
            )
            value_text_anchor = TextAnchor(
                text_segments=[
                    TextSpan(
                        offset=int(ts.start_index),
                        length=int(ts.end_index) - int(ts.start_index),
                    )
                    for ts in form_field.field_value.text_anchor.text_segments
                ]
            )

            # Use the bounding poly of the field_name for the overall field, or combine if necessary.
            bounding_poly_data = BoundingPoly(
                vertices=[
                    {"x": v.x, "y": v.y}
                    for v in form_field.field_name.bounding_poly.vertices
                ]
            )

            form_fields_data.append(
                DocumentPageFormProperty(
                    field_name=key_text_anchor,
                    field_value=value_text_anchor,
                    bounding_poly=bounding_poly_data,
                )
            )

        pages_data.append(
            DocumentPage(
                page_number=page.page_number,
                image_width=page.dimension.width,
                image_height=page.dimension.height,
                text=_get_text(document, page.layout.text_anchor),
                blocks=[],
                tables=[],
                form_fields=form_fields_data,
            )
        )

    # Also include entities from the overall document
    entities_data = []
    for entity in document.entities:
        entities_data.append(
            {
                "type": entity.type,
                "mention_text": entity.mention_text,
                "normalized_value": entity.normalized_value.text
                if entity.normalized_value
                else None,
            }
        )

    return DocumentResponse(
        text=document.text, pages=pages_data, entities=entities_data
    )
