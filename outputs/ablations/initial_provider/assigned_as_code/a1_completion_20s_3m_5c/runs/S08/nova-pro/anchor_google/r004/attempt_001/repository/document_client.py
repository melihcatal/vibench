from google.cloud import documentai

def get_documentai_client(config):
    client = documentai.DocumentProcessorServiceClient(
        client_options={"api_endpoint": f"{config['location']}-documentai.googleapis.com"})
    return client

def build_process_document_request(config, payload):
    client = get_documentai_client(config)
    name = client.processor_path(config["project_id"], config["location"], config["processor_id"])
    return {"name": name, "raw_document": documentai.RawDocument(
        content=payload["document_bytes"], mime_type=payload["mime_type"])}