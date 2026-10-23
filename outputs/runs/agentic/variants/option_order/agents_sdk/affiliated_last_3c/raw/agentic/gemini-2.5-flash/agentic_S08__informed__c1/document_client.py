import os
from google.cloud import documentai_v1beta3 as documentai
from google.api_core.client_options import ClientOptions

def get_document_ai_client(location: str = "us") -> documentai.DocumentProcessorServiceClient:
    """
    Provides a configured Google Document AI client.
    """
    opts = ClientOptions(api_endpoint=f"{location}-documentai.googleapis.com")
    return documentai.DocumentProcessorServiceClient(client_options=opts)

def get_processor_path(project_id: str, location: str, processor_id: str) -> str:
    """
    Constructs the full processor resource path.
    """
    client = get_document_ai_client(location)
    return client.processor_path(project_id, location, processor_id)


if __name__ == '__main__':
    # Example Usage
    project_id = os.getenv("GOOGLE_CLOUD_PROJECT", "your-gcp-project-id")
    location = "us"
    invoice_processor_id = os.getenv("GOOGLE_DOCAI_INVOICE_PROCESSOR_ID", "your-invoice-processor-id")

    print(f"Document AI Client for location: {location}")
    docai_client = get_document_ai_client(location)
    print(f"Processor path for invoice: {get_processor_path(project_id, location, invoice_processor_id)}")
