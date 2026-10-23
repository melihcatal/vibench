from google.cloud import documentai

def get_documentai_client(config):
    return documentai.DocumentProcessorServiceClient(
        client_options={"api_endpoint": f"{config['location']}-documentai.googleapis.com"})