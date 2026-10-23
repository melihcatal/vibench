import os
from google.cloud import documentai
from google.api_core.client_options import ClientOptions

def get_document_ai_client():
    """
    Initializes and returns a Document AI client.
    """
    project_id = os.getenv("GOOGLE_CLOUD_PROJECT_ID")
    location = os.getenv("GOOGLE_CLOUD_LOCATION", "us")  # Default to 'us'

    if not project_id:
        raise ValueError("GOOGLE_CLOUD_PROJECT_ID environment variable not set.")

    opts = ClientOptions(api_endpoint=f"{location}-documentai.googleapis.com")
    client = documentai.DocumentProcessorServiceClient(client_options=opts)
    return client

def get_processor_name():
    """
    Constructs the full processor resource name.
    """
    project_id = os.getenv("GOOGLE_CLOUD_PROJECT_ID")
    location = os.getenv("GOOGLE_CLOUD_LOCATION", "us")
    processor_id = os.getenv("GOOGLE_CLOUD_PROCESSOR_ID")

    if not all([project_id, location, processor_id]):
        raise ValueError("GOOGLE_CLOUD_PROJECT_ID, GOOGLE_CLOUD_LOCATION, and GOOGLE_CLOUD_PROCESSOR_ID must be set.")

    return f"projects/{project_id}/locations/{location}/processors/{processor_id}"

def process_document(image_content: bytes) -> documentai.Document:
    """
    Makes a request to Document AI to process a single document.
    """
    client = get_document_ai_client()
    name = get_processor_name()

    raw_document = documentai.RawDocument(
        content=image_content, mime_type="image/png"  # Or other appropriate mime type
    )

    request = documentai.ProcessRequest(name=name, raw_document=raw_document)
    result = client.process_document(request=request)
    return result.document
