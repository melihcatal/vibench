from google.cloud import documentai

def extract_key_values(payload, config=None):
    config = config or {}
    client = documentai.DocumentProcessorServiceClient(
        client_options={"api_endpoint": f"{config['location']}-documentai.googleapis.com"})
    name = client.processor_path(config["project_id"], config["location"], config["processor_id"])
    response = client.process_document(request={"name": name, "raw_document": documentai.RawDocument(
        content=payload["document_bytes"], mime_type=payload["mime_type"])})
    key_values = {}
    for entity in response.document.entities:
        if entity.type_ == documentai.Document.Entity.Type.KEY_VALUE_PAIR:
            key_values[entity.mention_text] = entity.normalized_value.string_value
    return {"key_values": key_values}