from google.cloud import documentai

def get_documentai_client(project_id: str, location: str) -> documentai.DocumentProcessorServiceClient:
    client_options = {"api_endpoint": f"{location}-documentai.googleapis.com"}
    client = documentai.DocumentProcessorServiceClient(client_options=client_options)
    return client
