from google.cloud import documentai
from document_client import build_client, processor_name
from document_models import normalize_layout


def extract_layout(payload, config=None):
    client, config = build_client(config)
    name = processor_name(client, config, config.get("layout_processor_id"))
    response = client.process_document(request={"name": name, "raw_document": documentai.RawDocument(content=payload["document_bytes"], mime_type=payload["mime_type"])})
    return normalize_layout(response.document)
