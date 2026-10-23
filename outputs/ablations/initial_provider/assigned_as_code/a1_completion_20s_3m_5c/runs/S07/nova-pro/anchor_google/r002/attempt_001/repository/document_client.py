from google.cloud import documentai


def get_document_client(config):
    return documentai.DocumentProcessorServiceClient(
        client_options={"api_endpoint": f"{config['location']}-documentai.googleapis.com"})


def get_processor_path(client, project_id, location, processor_id):
    return client.processor_path(project_id, location, processor_id)