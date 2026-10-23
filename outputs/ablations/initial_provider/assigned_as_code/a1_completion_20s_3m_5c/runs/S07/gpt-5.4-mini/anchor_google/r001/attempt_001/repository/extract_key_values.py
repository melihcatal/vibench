from google.cloud import documentai

from document_client import get_client, get_config, processor_path, raw_document


def extract_key_values(payload, config=None):
    config = get_config(config)
    client = get_client(config["location"])
    name = processor_path(client, config["project_id"], config["location"], config["form_processor_id"])
    response = client.process_document(request={"name": name, "raw_document": raw_document(payload)})
    document = response.document
    pairs = []
    for entity in document.entities:
        pairs.append({"key": entity.type_, "value": entity.mention_text})
    return {"key_values": pairs}
