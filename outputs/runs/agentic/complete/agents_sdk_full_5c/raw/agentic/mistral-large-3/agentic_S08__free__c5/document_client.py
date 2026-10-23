import os
from google.cloud import documentai_v1 as documentai
from google.api_core.client_options import ClientOptions


def get_document_client() -> documentai.DocumentProcessorServiceClient:
    client_options = ClientOptions(api_endpoint=f"us-documentai.googleapis.com")
    return documentai.DocumentProcessorServiceClient(client_options=client_options)


def get_processor_name(processor_id: str) -> str:
    project_id = os.getenv("GOOGLE_CLOUD_PROJECT_ID")
    return f"projects/{project_id}/locations/us/processors/{processor_id}"