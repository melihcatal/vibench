import os
from google.cloud import documentai_v1 as documentai

def get_document_ai_client():
    """Initializes and returns a Google Cloud Document AI client."""
    return documentai.DocumentProcessorServiceClient()

def get_processor_path(project_id: str, location: str, processor_id: str) -> str:
    """Constructs the full processor path for Document AI."""
    return f"projects/{project_id}/locations/{location}/processors/{processor_id}"

def get_gcs_input_uri(bucket_name: str, object_name: str) -> str:
    """Constructs a GCS input URI."""
    return f"gs://{bucket_name}/{object_name}"
