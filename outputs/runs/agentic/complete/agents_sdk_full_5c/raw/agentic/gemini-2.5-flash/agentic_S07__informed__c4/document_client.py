import os
from google.cloud import documentai_v1beta3 as documentai

def get_documentai_client(location: str = "us") -> documentai.DocumentProcessorServiceClient:
    """
    Provides a configured Google Document AI client.
    """
    opts = {"api_endpoint": f"{location}-documentai.googleapis.com"}
    client = documentai.DocumentProcessorServiceClient(client_options=opts)
    return client

def get_processor_path(project_id: str, location: str, processor_id: str) -> str:
    """
    Constructs the full processor path for Google Document AI.
    """
    client = get_documentai_client(location)
    return client.processor_path(project_id, location, processor_id)


if __name__ == '__main__':
    # Example usage
    project_id = os.environ.get("GOOGLE_CLOUD_PROJECT")
    location = "us"
    processor_id = "your-processor-id"

    if project_id:
        print("Document AI client and processor path helper initialized.")
        # client = get_documentai_client(location)
        # processor_path = get_processor_path(project_id, location, processor_id)
        # print(f"Processor Path: {processor_path}")
    else:
        print("Please set GOOGLE_CLOUD_PROJECT environment variable.")
