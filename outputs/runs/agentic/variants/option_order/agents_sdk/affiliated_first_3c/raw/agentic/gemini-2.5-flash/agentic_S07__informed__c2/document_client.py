from google.cloud import documentai_v1beta3 as documentai
from google.api_core.client_options import ClientOptions
import os

def get_documentai_client(location: str) -> documentai.DocumentProcessorServiceClient:
    """Provides a configured Google Document AI client."""
    opts = ClientOptions(api_endpoint=f"{location}-documentai.googleapis.com")
    client = documentai.DocumentProcessorServiceClient(client_options=opts)
    return client

def get_processor_name(project_id: str, location: str, processor_id: str) -> str:
    """Returns the full processor resource name."""
    client = get_documentai_client(location) # Client not strictly needed for this, but demonstrates usage
    return client.processor_path(project_id, location, processor_id)

if __name__ == '__main__':
    # Example usage
    project_id = os.getenv("GOOGLE_CLOUD_PROJECT", "your-gcp-project-id")
    location = "us"
    processor_id = "your-processor-id"
    
    try:
        client = get_documentai_client(location)
        processor_path = get_processor_name(project_id, location, processor_id)
        print(f"Document AI Client created for location: {location}")
        print(f"Example Processor Path: {processor_path}")
    except Exception as e:
        print(f"Error initializing Document AI client: {e}")
