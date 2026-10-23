from google.cloud import documentai

def get_documentai_client(location: str):
    return documentai.DocumentProcessorServiceClient(
        client_options={"api_endpoint": f"{location}-documentai.googleapis.com"})
