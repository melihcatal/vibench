from google.cloud import documentai

from document_client import load_config, make_client, processor_name, raw_document
from document_models import normalize_key_values


def extract_key_values(payload, config=None):
    config = load_config(config)
    client = make_client(config)
    name = processor_name(client, config)
    response = client.process_document(request={"name": name, "raw_document": raw_document(payload)})
    pairs = []
    for page in response.document.pages:
        for kv in page.form_fields:
            key = kv.field_name.text_anchor.content if kv.field_name.text_anchor else ""
            value = kv.field_value.text_anchor.content if kv.field_value.text_anchor else ""
            pairs.append({"key": key, "value": value})
    return {"key_values": normalize_key_values(pairs)}
