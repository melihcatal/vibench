import os
from google.cloud import documentai_v1beta3 as documentai


def get_documentai_client():
    # Google Cloud Document AI client setup
    # Ensure GOOGLE_APPLICATION_CREDENTIALS environment variable is set
    return documentai.DocumentProcessorServiceClient()


def process_document(
    project_id: str,
    location: str,
    processor_id: str,
    file_content: bytes,
    mime_type: str,
):
    client = get_documentai_client()
    name = client.processor_path(project_id, location, processor_id)

    # Read the file into memory
    raw_document = documentai.RawDocument(content=file_content, mime_type=mime_type)

    # Configure the process request
    request = documentai.ProcessRequest(name=name, raw_document=raw_document)

    result = client.process_document(request=request)
    return result.document
