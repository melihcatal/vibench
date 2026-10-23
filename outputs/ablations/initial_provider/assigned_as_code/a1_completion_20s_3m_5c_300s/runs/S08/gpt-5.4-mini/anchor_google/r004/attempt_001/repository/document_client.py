import os
from google.cloud import documentai

from document_models import DocumentRequest, normalize_response


def load_documentai_config(config=None):
    config = config or {}
    return {
        "project_id": config.get("project_id") or os.environ.get("GOOGLE_CLOUD_PROJECT"),
        "location": config.get("location") or os.environ.get("DOCUMENTAI_LOCATION", "us"),
        "processor_id": config.get("processor_id") or os.environ.get("DOCUMENTAI_PROCESSOR_ID"),
    }


def get_documentai_client(config=None):
    config = load_documentai_config(config)
    return documentai.DocumentProcessorServiceClient(
        client_options={"api_endpoint": f"{config['location']}-documentai.googleapis.com"}
    ), config


def process_document(payload, config=None):
    client, config = get_documentai_client(config)
    request = payload if isinstance(payload, DocumentRequest) else DocumentRequest(**payload)
    name = client.processor_path(config["project_id"], config["location"], config["processor_id"])
    response = client.process_document(
        request={"name": name, "raw_document": documentai.RawDocument(content=request.document_bytes, mime_type=request.mime_type)}
    )
    return response


def document_entities_to_response(response):
    fields, items = {}, []
    for entity in response.document.entities:
        if entity.type_ == "line_item":
            values = {p.type_.split("/")[-1]: p.mention_text for p in entity.properties}
            items.append({"description": values.get("description"), "quantity": values.get("quantity"), "amount": values.get("amount")})
        else:
            fields[entity.type_] = entity.mention_text
    return normalize_response(fields=fields, items=items, raw=response)
