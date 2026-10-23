import os

from google.cloud import documentai


def load_documentai_config(config=None):
    config = dict(config or {})
    config.setdefault("project_id", os.environ.get("GOOGLE_CLOUD_PROJECT"))
    config.setdefault("location", os.environ.get("DOCUMENTAI_LOCATION", "us"))
    config.setdefault("processor_id", os.environ.get("DOCUMENTAI_PROCESSOR_ID"))
    return config


def get_documentai_client(config):
    return documentai.DocumentProcessorServiceClient(
        client_options={"api_endpoint": f"{config['location']}-documentai.googleapis.com"}
    )


def process_document_bytes(document_bytes, mime_type, config):
    client = get_documentai_client(config)
    name = client.processor_path(config["project_id"], config["location"], config["processor_id"])
    return client.process_document(
        request={"name": name, "raw_document": documentai.RawDocument(content=document_bytes, mime_type=mime_type)}
    )
