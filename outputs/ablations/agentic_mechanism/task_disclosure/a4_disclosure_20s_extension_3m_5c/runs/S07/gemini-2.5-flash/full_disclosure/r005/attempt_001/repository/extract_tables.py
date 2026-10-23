from google.cloud import documentai_v1beta3 as documentai
from google.api_core.client_options import ClientOptions
import os

def extract_tables_from_document(
    project_id: str,
    location: str,
    processor_id: str,
    file_path: str = None,
    file_content: bytes = None,
    mime_type: str = "application/pdf",
):
    """
    Extracts table cells and row structure from a document using Google Cloud Document AI.

    Args:
        project_id: Your Google Cloud project ID.
        location: The Google Cloud region (e.g., "us").
        processor_id: The ID of the Document AI table extraction processor.
        file_path: The path to the document file.
        file_content: The content of the document file as bytes.
        mime_type: The MIME type of the document (e.g., "application/pdf").

    Returns:
        A document object with extracted tables.
    """
    opts = ClientOptions(api_endpoint=f"{location}-documentai.googleapis.com")
    client = documentai.DocumentProcessorServiceClient(client_options=opts)

    if file_path:
        with open(file_path, "rb") as image:
            image_content = image.read()
    elif file_content:
        image_content = file_content
    else:
        raise ValueError("Either file_path or file_content must be provided.")

    raw_document = documentai.RawDocument(content=image_content, mime_type=mime_type)

    name = client.processor_path(project_id, location, processor_id)
    request = documentai.ProcessRequest(name=name, raw_document=raw_document)

    result = client.process_document(request=request)
    return result.document
