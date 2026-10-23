import os
from google.cloud import documentai_v1 as documentai
from google.api_core.client_options import ClientOptions
from document_client import get_google_document_ai_client
from document_models import DocumentInput, KeyValueExtractionResult, KeyValuePair, BoundingBox

def extract_key_values_from_document(doc_input: DocumentInput) -> KeyValueExtractionResult:
    project_id = os.environ.get("GOOGLE_CLOUD_PROJECT_ID")
    location = os.environ.get("GOOGLE_CLOUD_LOCATION", "us")
    processor_id = os.environ.get("GOOGLE_CLOUD_DOCUMENT_AI_PROCESSOR_ID")

    if not project_id or not processor_id:
        raise ValueError("GOOGLE_CLOUD_PROJECT_ID and GOOGLE_CLOUD_DOCUMENT_AI_PROCESSOR_ID must be set.")

    client = get_google_document_ai_client()

    processor_name = client.processor_path(project_id, location, processor_id)

    raw_document = documentai.RawDocument(
        content=doc_input.document_bytes,
        mime_type=doc_input.mime_type,
    )

    request = documentai.ProcessRequest(name=processor_name, raw_document=raw_document)

    response = client.process_document(request=request)
    document = response.document

    extracted_key_values: list[KeyValuePair] = []

    for page in document.pages:
        for form_field in page.form_fields:
            key_text = form_field.field_name.text_segment.content if form_field.field_name.text_segment else ""
            value_text = form_field.field_value.text_segment.content if form_field.field_value.text_segment else ""
            
            key_bbox = None
            if form_field.field_name.bounding_poly and form_field.field_name.bounding_poly.vertices:
                vertices = form_field.field_name.bounding_poly.vertices
                key_bbox = BoundingBox(
                    x1=min(v.x for v in vertices), y1=min(v.y for v in vertices),
                    x2=max(v.x for v in vertices), y2=max(v.y for v in vertices)
                )

            value_bbox = None
            if form_field.field_value.bounding_poly and form_field.field_value.bounding_poly.vertices:
                vertices = form_field.field_value.bounding_poly.vertices
                value_bbox = BoundingBox(
                    x1=min(v.x for v in vertices), y1=min(v.y for v in vertices),
                    x2=max(v.x for v in vertices), y2=max(v.y for v in vertices)
                )
            
            confidence = form_field.field_value.confidence if hasattr(form_field.field_value, 'confidence') else None

            extracted_key_values.append(
                KeyValuePair(
                    key=key_text,
                    value=value_text,
                    key_bounding_box=key_bbox,
                    value_bounding_box=value_bbox,
                    confidence=confidence
                )
            )
            
    return KeyValueExtractionResult(key_value_pairs=extracted_key_values)