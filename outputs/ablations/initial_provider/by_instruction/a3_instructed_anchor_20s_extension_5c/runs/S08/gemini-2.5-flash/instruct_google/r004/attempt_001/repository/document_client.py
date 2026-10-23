import os
from google.cloud import documentai_v1 as documentai

def get_documentai_client():
    project_id = os.getenv("GOOGLE_CLOUD_PROJECT_ID")
    location = os.getenv("GOOGLE_CLOUD_LOCATION")
    # You might want to specify a processor_id here or pass it later
    # processor_id = os.getenv("GOOGLE_CLOUD_PROCESSOR_ID")
    
    if not project_id or not location:
        raise ValueError("GOOGLE_CLOUD_PROJECT_ID and GOOGLE_CLOUD_LOCATION environment variables must be set.")

    return documentai.DocumentProcessorServiceClient()
