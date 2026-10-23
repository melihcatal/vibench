from google.cloud import documentai_v1 as documentai
import os


def get_documentai_client():
    # Google Cloud Project ID
    project_id = os.getenv("GOOGLE_CLOUD_PROJECT")
    if not project_id:
        raise ValueError("GOOGLE_CLOUD_PROJECT environment variable not set.")

    client_options = {"api_endpoint": "us-documentai.googleapis.com"}
    client = documentai.DocumentProcessorServiceClient(client_options=client_options)
    return client
