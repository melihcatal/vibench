from google.cloud import documentai

from document_models import build_request


def get_documentai_client(config):
    return documentai.DocumentProcessorServiceClient(
        client_options={"api_endpoint": f"{config['location']}-documentai.googleapis.com"}
    )


def process_document(payload, config):
    request = build_request(payload)
    client = get_documentai_client(config)
    name = client.processor_path(config["project_id"], config["location"], config["processor_id"])
    return client.process_document(
        request={
            "name": name,
            "raw_document": documentai.RawDocument(content=request.document_bytes, mime_type=request.mime_type),
        }
    )
