from google.cloud import documentai

from document_client import normalize_config, make_documentai_client
from document_models import normalize_key_value_pairs


def extract_key_values(payload, config=None):
    config = normalize_config(config)
    client = make_documentai_client(config["location"])
    name = client.processor_path(config["project_id"], config["location"], config["processor_id"])
    response = client.process_document(request={"name": name, "raw_document": documentai.RawDocument(content=payload["document_bytes"], mime_type=payload["mime_type"])})
    pairs = []
    for page in response.document.pages:
        for form_field in page.form_fields:
            pairs.append({"key": form_field.field_name.text_anchor.content if hasattr(form_field.field_name.text_anchor, "content") else "", "value": form_field.field_value.text_anchor.content if hasattr(form_field.field_value.text_anchor, "content") else ""})
    return {"key_values": normalize_key_value_pairs(pairs)}
