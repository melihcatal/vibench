from google.cloud import documentai


def load_config(config=None):
    config = config or {}
    return {
        "project_id": config.get("project_id"),
        "location": config.get("location", "us"),
        "processor_id": config.get("processor_id"),
        "language": config.get("language", "en"),
        "gcs_uri": config.get("gcs_uri"),
        "mime_type": config.get("mime_type", "application/pdf"),
    }


def make_client(config):
    return documentai.DocumentProcessorServiceClient(client_options={"api_endpoint": f"{config['location']}-documentai.googleapis.com"})


def processor_name(client, config):
    return client.processor_path(config["project_id"], config["location"], config["processor_id"])


def raw_document(payload):
    return documentai.RawDocument(content=payload["document_bytes"], mime_type=payload["mime_type"])
