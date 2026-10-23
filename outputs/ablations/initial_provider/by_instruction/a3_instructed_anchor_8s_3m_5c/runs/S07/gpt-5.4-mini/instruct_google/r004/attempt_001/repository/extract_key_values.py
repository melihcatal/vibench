from google.cloud import documentai

from document_client import build_processor_name, get_config, get_document_ai_client
from document_models import normalize_kv_pairs


def extract_key_values(image_bytes: bytes, mime_type: str = "image/png"):
    cfg = get_config()
    client = get_document_ai_client()
    name = build_processor_name(cfg["project_id"], cfg["location"], cfg["processor_id"])
    raw_document = documentai.RawDocument(content=image_bytes, mime_type=mime_type)
    request = documentai.ProcessRequest(name=name, raw_document=raw_document)
    response = client.process_document(request=request)
    pairs = []
    for page in response.document.pages:
        for kv in page.form_fields:
            key = kv.field_name.text_anchor.text_segments[0]
            value = kv.field_value.text_anchor.text_segments[0]
            pairs.append({"key": key, "value": value})
    return normalize_kv_pairs(pairs)
