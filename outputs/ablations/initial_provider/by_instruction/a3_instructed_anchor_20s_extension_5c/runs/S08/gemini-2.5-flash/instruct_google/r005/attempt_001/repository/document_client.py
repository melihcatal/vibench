import os
from google.cloud import documentai_v1 as documentai
from google.api_core.client_options import ClientOptions

def get_documentai_client():
    # https://cloud.google.com/document-ai/docs/reference/rest/v1/projects.locations.processors/process
    # https://cloud.google.com/python/docs/reference/documentai/latest
    
    # It's recommended to set GOOGLE_APPLICATION_CREDENTIALS environment variable.
    # For local development, you might set it like:
    # os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "/path/to/your/keyfile.json"

    client_options = ClientOptions(api_endpoint=f"{os.environ.get('GOOGLE_CLOUD_REGION', 'us')}-documentai.googleapis.com")
    client = documentai.DocumentProcessorServiceClient(client_options=client_options)
    return client

def process_document_with_documentai(
    project_id: str,
    location: str,
    processor_id: str,
    file_content: bytes,
    mime_type: str,
):
    client = get_documentai_client()

    name = client.processor_path(project_id, location, processor_id)

    raw_document = documentai.RawDocument(
        content=file_content,
        mime_type=mime_type,
    )

    request = documentai.ProcessRequest(
        name=name,
        raw_document=raw_document,
    )

    result = client.process_document(request=request)
    return result.document
