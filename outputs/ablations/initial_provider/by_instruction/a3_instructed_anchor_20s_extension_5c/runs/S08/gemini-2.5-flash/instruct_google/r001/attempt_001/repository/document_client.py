import os
from google.cloud import documentai

def get_documentai_client():
    project_id = os.environ.get("GOOGLE_CLOUD_PROJECT_ID")
    location = os.environ.get("GOOGLE_CLOUD_LOCATION") # e.g., "us"
    processor_id = os.environ.get("GOOGLE_CLOUD_DOCUMENTAI_INVOICE_PROCESSOR_ID")

    if not all([project_id, location, processor_id]):
        raise ValueError("Missing Google Cloud Document AI environment variables: GOOGLE_CLOUD_PROJECT_ID, GOOGLE_CLOUD_LOCATION, GOOGLE_CLOUD_DOCUMENTAI_INVOICE_PROCESSOR_ID")

    # The Document AI client libraries automatically handle authentication with Application Default Credentials
    # Ensure GOOGLE_APPLICATION_CREDENTIALS environment variable is set or running in a GCP environment
    client = documentai.DocumentProcessorServiceClient()

    processor_name = client.processor_path(project_id, location, processor_id)
    
    return client, processor_name

def get_documentai_receipt_client():
    project_id = os.environ.get("GOOGLE_CLOUD_PROJECT_ID")
    location = os.environ.get("GOOGLE_CLOUD_LOCATION") # e.g., "us"
    processor_id = os.environ.get("GOOGLE_CLOUD_DOCUMENTAI_RECEIPT_PROCESSOR_ID")

    if not all([project_id, location, processor_id]):
        raise ValueError("Missing Google Cloud Document AI environment variables: GOOGLE_CLOUD_PROJECT_ID, GOOGLE_CLOUD_LOCATION, GOOGLE_CLOUD_DOCUMENTAI_RECEIPT_PROCESSOR_ID")

    client = documentai.DocumentProcessorServiceClient()

    processor_name = client.processor_path(project_id, location, processor_id)
    
    return client, processor_name
