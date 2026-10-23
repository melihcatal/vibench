import os
from google.cloud import documentai_v1 as documentai


def get_documentai_client():
    # Ensure GOOGLE_APPLICATION_CREDENTIALS is set in the environment
    # For local development, this typically points to a service account key file.
    # In Google Cloud environments (e.g., Cloud Functions, Cloud Run),
    # credentials are automatically handled by the environment.
    return documentai.DocumentProcessorServiceClient()


def get_processor_name(project_id: str, location: str, processor_id: str) -> str:
    return get_documentai_client().processor_path(project_id, location, processor_id)


# Placeholder for other client initializations if needed later
