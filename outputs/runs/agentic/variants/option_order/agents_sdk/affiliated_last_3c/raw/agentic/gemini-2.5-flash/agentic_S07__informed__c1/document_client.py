import os
from google.cloud import documentai_v1 as documentai

def get_document_ai_client(location: str):
    """
    Returns a configured Google Document AI client.
    """
    opts = {"api_endpoint": f"{location}-documentai.googleapis.com"}
    client = documentai.DocumentProcessorServiceClient(client_options=opts)
    return client

def get_processor_name(project_id: str, location: str, processor_id: str) -> str:
    """
    Returns the full resource name of the Document AI processor.
    """
    client = get_document_ai_client(location) # Client needed to use processor_path utility
    return client.processor_path(project_id, location, processor_id)


# Example usage (not part of the module's core function but for demonstration)
if __name__ == '__main__':
    project_id = os.environ.get("GOOGLE_CLOUD_PROJECT")
    location = "us"
    processor_id = os.environ.get("DOCUMENT_AI_PROCESSOR_ID_OCR")

    if project_id and processor_id:
        print(f"Document AI Client for location: {location}")
        client = get_document_ai_client(location)
        print(f"Processor Name: {get_processor_name(project_id, location, processor_id)}")
    else:
        print("Please set GOOGLE_CLOUD_PROJECT and DOCUMENT_AI_PROCESSOR_ID_OCR environment variables.")
