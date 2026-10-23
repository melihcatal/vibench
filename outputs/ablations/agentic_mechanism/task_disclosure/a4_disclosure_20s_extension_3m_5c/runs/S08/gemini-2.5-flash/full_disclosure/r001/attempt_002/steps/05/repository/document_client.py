import os
from google.cloud import documentai_v1 as documentai

def get_documentai_client():
    """Returns a Document AI client."""
    return documentai.DocumentProcessorServiceClient()

def process_document(
    project_id: str,
    location: str,
    processor_id: str,
    file_path: str,
    mime_type: str,
):
    """Processes a document using the Document AI client.

    Args:
        project_id: Your Google Cloud project ID.
        location: The Document AI processor location (e.g., "us").
        processor_id: The ID of the processor to use.
        file_path: The path to the document file.
        mime_type: The MIME type of the document (e.g., "application/pdf").

    Returns:
        documentai.Document: The processed document.
    """
    client = get_documentai_client()
    name = client.processor_path(project_id, location, processor_id)

    with open(file_path, "rb") as image:
        image_content = image.read()

    raw_document = documentai.RawDocument(content=image_content, mime_type=mime_type)
    request = documentai.ProcessRequest(name=name, raw_document=raw_document)

    result = client.process_document(request=request)
    return result.document

