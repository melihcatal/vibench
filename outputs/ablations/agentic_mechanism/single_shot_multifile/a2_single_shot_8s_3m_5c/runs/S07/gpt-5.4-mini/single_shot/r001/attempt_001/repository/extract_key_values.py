from google.cloud import documentai
from document_client import get_document_ai_client, get_document_ai_processor_name
from document_models import DocumentKVPRequest, KeyValuePair, KeyValueResponse, bbox_to_dict


def extract_key_values(request: DocumentKVPRequest) -> KeyValueResponse:
    client = get_document_ai_client()
    name = get_document_ai_processor_name(request.processor_id, request.location, request.project_id)
    raw_document = documentai.RawDocument(content=request.image_bytes, mime_type=request.mime_type)
    doc = client.process_document(name=name, raw_document=raw_document)
    pairs = []
    for page in doc.document.pages:
        for form_field in page.form_fields:
            key = form_field.field_name.text_anchor.content if form_field.field_name.text_anchor else ""
            value = form_field.field_value.text_anchor.content if form_field.field_value.text_anchor else ""
            pairs.append(KeyValuePair(key=key, value=value, key_bbox=bbox_to_dict(form_field.field_name.bounding_poly), value_bbox=bbox_to_dict(form_field.field_value.bounding_poly)))
    return KeyValueResponse(pairs=pairs, raw=doc)
