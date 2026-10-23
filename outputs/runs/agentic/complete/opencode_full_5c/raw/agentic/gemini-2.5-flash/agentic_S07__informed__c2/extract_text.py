import os
from typing import Tuple

from google.cloud import documentai_v1 as documentai
from google.api_core.client_options import ClientOptions

from document_client import get_documentai_client
from document_models import ExtractedText


def extract_text_from_document(
    project_id: str, location: str, processor_id: str, file_path: str, mime_type: str
) -> ExtractedText:
    """Extracts plain text from a document using Google Document AI.

    Args:
        project_id: Your Google Cloud project ID.
        location: The Document AI processor location (e.g., "us").
        processor_id: The ID of the OCR processor to use.
        file_path: The path to the document file.
        mime_type: The MIME type of the document (e.g., "application/pdf").

    Returns:
        An ExtractedText object containing the plain text content.
    """
    client = get_documentai_client()

    # The full resource name of the processor
    # e.g.: projects/project_id/locations/location/processors/processor_id
    resource_name = client.processor_path(project_id, location, processor_id)

    with open(file_path, "rb") as image_file:
        content = image_file.read()

    raw_document = documentai.RawDocument(content=content, mime_type=mime_type)

    # Configure the process request
    request = documentai.ProcessRequest(name=resource_name, raw_document=raw_document)

    result = client.process_document(request=request)

    document = result.document
    return ExtractedText(text_content=document.text)
