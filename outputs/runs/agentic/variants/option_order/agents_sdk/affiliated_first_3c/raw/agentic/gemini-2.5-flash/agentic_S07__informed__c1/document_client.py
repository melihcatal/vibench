import os
from google.cloud import documentai_v1 as documentai

def get_documentai_client():
    """Returns a Document AI client."""
    return documentai.DocumentProcessorServiceClient()

def get_processor_path(project_id: str, location: str, processor_id: str) -> str:
    """Returns the full resource path for a Document AI processor."""
    return f"projects/{project_id}/locations/{location}/processors/{processor_id}"

def get_documentai_client_with_endpoint(api_endpoint: str):
    """Returns a Document AI client with a custom API endpoint."""
    # Example: api_endpoint = "us-documentai.googleapis.com"
    return documentai.DocumentProcessorServiceClient(client_options={"api_endpoint": api_endpoint})
