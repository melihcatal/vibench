import os
from google.cloud import documentai


def get_documentai_client():
    """Provides a configured Google Cloud Document AI client."""
    # Google Cloud client libraries automatically use GOOGLE_APPLICATION_CREDENTIALS
    # environment variable for authentication.
    return documentai.DocumentProcessorServiceClient()


def get_processor_name(project_id: str, location: str, processor_id: str) -> str:
    """Constructs the full processor resource name."""
    return f"projects/{project_id}/locations/{location}/processors/{processor_id}"
