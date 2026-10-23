import os
from google.cloud import documentai_v1 as documentai

def get_documentai_client():
    # Google Cloud project ID and location
    project_id = os.environ.get("GOOGLE_CLOUD_PROJECT_ID")
    location = os.environ.get("GOOGLE_CLOUD_LOCATION", "us") # Default to 'us'

    if not project_id:
        raise ValueError("GOOGLE_CLOUD_PROJECT_ID environment variable not set.")

    client = documentai.DocumentProcessorServiceClient()
    return client, project_id, location

def get_processor_name(project_id: str, location: str, processor_id: str):
    return f"projects/{project_id}/locations/{location}/processors/{processor_id}"
