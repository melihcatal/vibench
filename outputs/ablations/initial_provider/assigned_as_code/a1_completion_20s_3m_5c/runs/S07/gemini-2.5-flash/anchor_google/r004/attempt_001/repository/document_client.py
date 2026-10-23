from google.cloud import documentai

def get_documentai_client(location: str):
    return documentai.DocumentProcessorServiceClient(
        client_options={"api_endpoint": f"{location}-documentai.googleapis.com"})

def get_processor_path(project_id: str, location: str, processor_id: str):
    client = get_documentai_client(location) # Client is used here only for path construction
    return client.processor_path(project_id, location, processor_id)
