from google.cloud import documentai


def build_document_ai_client(config):
    location = config["location"]
    return documentai.DocumentProcessorServiceClient(
        client_options={"api_endpoint": f"{location}-documentai.googleapis.com"}
    )


def build_processor_name(config):
    return documentai.DocumentProcessorServiceClient().processor_path(
        config["project_id"], config["location"], config["processor_id"]
    )


def build_raw_document(payload):
    return documentai.RawDocument(
        content=payload["document_bytes"], mime_type=payload["mime_type"]
    )
