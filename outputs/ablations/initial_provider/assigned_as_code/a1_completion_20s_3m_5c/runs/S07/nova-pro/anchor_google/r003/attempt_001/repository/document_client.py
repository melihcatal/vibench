import os
from google.cloud import documentai

def get_document_client(project_id, location, processor_id):
    return documentai.DocumentProcessorServiceClient(
        client_options={"api_endpoint": f"{location}-documentai.googleapis.com"})