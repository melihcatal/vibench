from google.cloud import documentai_v1 as documentai
from document_client import get_documentai_client, get_project_id, get_location, DOCUMENT_AI_PROCESSOR_FORM_PARSER
from document_models import KeyValuePair

def extract_key_value_pairs(document_bytes: bytes, mime_type: str) -> list[KeyValuePair]:
    project_id = get_project_id()
    location = get_location()
    processor_id = DOCUMENT_AI_PROCESSOR_FORM_PARSER
    client = get_documentai_client()
    processor_name = client.processor_path(project_id, location, processor_id)
    raw_document = documentai.RawDocument(content=document_bytes, mime_type=mime_type)
    request = documentai.ProcessRequest(name=processor_name, raw_document=raw_document)
    response = client.process_document(request=request)
    document = response.document
    extracted_kv_pairs: list[KeyValuePair] = []
    def get_text_from_span(text_segments, document_text):
        if not text_segments:
            return ""
        start_index = text_segments[0].start_index
        end_index = text_segments[0].end_index
        return document_text[start_index:end_index] if start_index is not None and end_index is not None else ""
    def convert_bounding_poly(bounding_poly) -> list[list[int]]:
        if not bounding_poly or not bounding_poly.vertices:
            return []
        return [[vertex.x, vertex.y] for vertex in bounding_poly.vertices]
    for page in document.pages:
        for form_field in page.form_fields:
            key_text = get_text_from_span(form_field.field_name.text_anchor.text_segments, document.text)
            value_text = get_text_from_span(form_field.field_value.text_anchor.text_segments, document.text)
            extracted_kv_pairs.append(KeyValuePair(
                key=key_text,
                value=value_text,
                key_bounding_boxes=convert_bounding_poly(form_field.field_name.bounding_poly),
                value_bounding_boxes=convert_bounding_poly(form_field.field_value.bounding_poly),
                confidence=form_field.field_value.confidence
            ))
    return extracted_kv_pairs