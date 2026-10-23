import os
from google.cloud import documentai


def get_document_client():
    config = {
        "project_id": os.getenv('GOOGLE_CLOUD_PROJECT_ID'),
        "location": os.getenv('GOOGLE_CLOUD_LOCATION'),
        "processor_id": os.getenv('GOOGLE_CLOUD_PROCESSOR_ID')
    }
    return documentai.DocumentProcessorServiceClient(
        client_options={"api_endpoint": f"{config['location']}-documentai.googleapis.com"})
