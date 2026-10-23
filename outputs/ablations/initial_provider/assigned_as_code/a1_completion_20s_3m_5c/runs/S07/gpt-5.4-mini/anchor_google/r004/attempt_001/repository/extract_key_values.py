from google.cloud import documentai

from document_client import build_document_ai_client, build_raw_document
from document_models import normalize_key_value_pairs


def extract_key_values(payload, config=None):
    config = config or {}
    client = build_document_ai_client(config)
    name = client.processor_path(config["project_id"], config["location"], config["processor_id"])
    response = client.process_document(request={"name": name, "raw_document": build_raw_document(payload)})
    return {"key_values": normalize_key_value_pairs(response.document)}
