from google.cloud import documentai

from document_client import build_document_ai_client, build_raw_document
from document_models import normalize_blocks


def extract_layout(payload, config=None):
    config = config or {}
    client = build_document_ai_client(config)
    name = client.processor_path(config["project_id"], config["location"], config["processor_id"])
    response = client.process_document(request={"name": name, "raw_document": build_raw_document(payload)})
    doc = response.document
    return {"blocks": normalize_blocks(getattr(doc, "pages", [])[0].blocks if getattr(doc, "pages", None) else [])}
