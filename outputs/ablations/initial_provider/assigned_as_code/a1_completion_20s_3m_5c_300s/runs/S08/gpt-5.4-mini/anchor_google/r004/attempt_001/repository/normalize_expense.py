from google.cloud import documentai


def normalize_expense(payload, config=None):
    config = config or {}
    client = documentai.DocumentProcessorServiceClient(
        client_options={"api_endpoint": f"{config['location']}-documentai.googleapis.com"})
    name = client.processor_path(config["project_id"], config["location"], config["processor_id"])
    response = client.process_document(request={"name": name, "raw_document": documentai.RawDocument(
        content=payload["document_bytes"], mime_type=payload["mime_type"])})
    document = response.document
    normalized = {"merchant": None, "date": None, "currency": None, "total": None, "items": []}
    for entity in document.entities:
        if entity.type_ in normalized and entity.type_ != "items":
            normalized[entity.type_] = entity.mention_text
        elif entity.type_ == "line_item":
            values = {p.type_.split("/")[-1]: p.mention_text for p in entity.properties}
            normalized["items"].append(values)
    return {"expense": normalized}
