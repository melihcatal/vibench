from google.cloud import documentai

from document_client import get_client, get_config, processor_path, raw_document
from document_models import normalize_sections


def document_field_extraction(payload, config=None):
    config = get_config(config)
    client = get_client(config["location"])
    name = processor_path(client, config["project_id"], config["location"], config["form_processor_id"])
    response = client.process_document(request={"name": name, "raw_document": raw_document(payload)})
    document = response.document
    fields = []
    for entity in document.entities:
        fields.append({"section": entity.type_, "text": entity.mention_text})
    return normalize_sections(fields)
