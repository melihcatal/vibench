import os
from google.cloud import documentai_v1 as documentai

def get_documentai_client():
    """Provides a Google Document AI client."""
    # Ensure GOOGLE_APPLICATION_CREDENTIALS environment variable is set or configure authentication
    return documentai.DocumentProcessorServiceClient()

def get_processor_path(project_id: str, location: str, processor_id: str) -> str:
    """Constructs the full processor path."""
    return f"projects/{project_id}/locations/{location}/processors/{processor_id}"

