from google.cloud import documentai
from google.api_core.client_options import ClientOptions
import os


def get_document_ai_client():
    project_id = os.getenv("GOOGLE_CLOUD_PROJECT")
    location = "us"  # e.g., "us" or "eu"
    processor_id = os.getenv(
        "DOCUMENTAI_PROCESSOR_ID"
    )  # Specific processor ID for invoice or receipt

    if not all([project_id, location, processor_id]):
        raise ValueError("Missing Google Cloud or Document AI configuration.")

    opts = ClientOptions(api_endpoint=f"{location}-documentai.googleapis.com")
    client = documentai.DocumentProcessorServiceClient(client_options=opts)

    name = client.processor_path(project_id, location, processor_id)
    return client, name
