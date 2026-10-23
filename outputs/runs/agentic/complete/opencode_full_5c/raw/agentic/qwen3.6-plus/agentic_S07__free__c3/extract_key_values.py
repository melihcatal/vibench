from document_client import get_google_document_ai_client
from document_models import (
    KeyValueResponse,
    KeyValue,
    BoundingBox,
    normalize_bounding_box,
    normalize_confidence,
)

GOOGLE_DOC_AI_FORM_PROCESSOR_TYPE = "form-parser"
GOOGLE_DOC_AI_FORM_MODEL_ID = "builtin/latest"


def extract_key_values_from_document(
    document_bytes: bytes,
    mime_type: str = "application/pdf",
) -> KeyValueResponse:
    client, project_id, location = get_google_document_ai_client()

    processor_display_name = "form-parser-processor"
    processors = client.list_processors(
        parent=f"projects/{project_id}/locations/{location}"
    )
    processor_name = None
    for proc in processors:
        if proc.display_name == processor_display_name:
            processor_name = proc.name
            break

    if processor_name is None:
        raise ValueError(
            f"Processor '{processor_display_name}' not found. "
            f"Create a {GOOGLE_DOC_AI_FORM_PROCESSOR_TYPE} processor in Google Cloud Document AI."
        )

    from google.cloud.documentai_v1 import ProcessRequest
    from google.cloud.documentai_v1.types import document as doc_types

    raw_document = doc_types.RawDocument(
        content=document_bytes,
        mime_type=mime_type,
    )

    request = ProcessRequest(
        name=processor_name,
        raw_document=raw_document,
    )

    result = client.process_document(request=request)
    document = result.document

    key_values = []

    for page in document.pages:
        for form_field in page.form_fields:
            field_name = _extract_field_name_text(document, form_field.field_name)
            field_value = _extract_field_value_text(document, form_field.field_value)

            key_bbox = _parse_google_bounding_box(form_field.field_name.bounding_poly)
            value_bbox = _parse_google_bounding_box(
                form_field.field_value.bounding_poly
            )

            confidence = normalize_confidence(form_field.confidence)

            kv = KeyValue(
                key=field_name,
                value=field_value,
                confidence=confidence,
                key_bounding_box=key_bbox,
                value_bounding_box=value_bbox,
            )
            key_values.append(kv)

    page_width = 1.0
    page_height = 1.0
    if document.pages:
        dim = document.pages[0].dimension
        page_width = dim.width
        page_height = dim.height

    return KeyValueResponse(
        key_values=key_values,
        page_width=page_width,
        page_height=page_height,
    )


def _extract_field_name_text(document, field_name) -> str:
    text = ""
    if field_name.text_anchor and field_name.text_anchor.text_segments:
        for segment in field_name.text_anchor.text_segments:
            text += document.text[segment.start_index : segment.end_index]
    return text.strip()


def _extract_field_value_text(document, field_value) -> str:
    text = ""
    if field_value.text_anchor and field_value.text_anchor.text_segments:
        for segment in field_value.text_anchor.text_segments:
            text += document.text[segment.start_index : segment.end_index]
    return text.strip()


def _parse_google_bounding_box(bounding_poly) -> BoundingBox:
    if not bounding_poly or not bounding_poly.vertices:
        return BoundingBox(x=0.0, y=0.0, width=0.0, height=0.0)
    points = [(v.x, v.y) for v in bounding_poly.vertices]
    return normalize_bounding_box(points)
