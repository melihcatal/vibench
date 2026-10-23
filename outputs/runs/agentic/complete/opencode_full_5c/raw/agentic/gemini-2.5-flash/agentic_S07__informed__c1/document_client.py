from google.cloud import documentai_v1b3 as documentai
import os


def get_document_ai_client(location: str):
    """Returns a Google Document AI client configured for the given location."""
    opts = {"api_endpoint": f"{location}-documentai.googleapis.com"}
    client = documentai.DocumentProcessorServiceClient(client_options=opts)
    return client


def get_processor_path(client, project_id: str, location: str, processor_id: str):
    """Returns the full processor path for Google Document AI."""
    return client.processor_path(project_id, location, processor_id)


def create_raw_document(file_content: bytes, mime_type: str):
    """Creates a RawDocument object for Document AI."""
    return documentai.RawDocument(content=file_content, mime_type=mime_type)
