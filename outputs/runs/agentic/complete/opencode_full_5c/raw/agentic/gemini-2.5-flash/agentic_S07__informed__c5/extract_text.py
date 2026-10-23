from google.cloud import documentai_v1beta3 as documentai
import os
from document_client import get_documentai_client


def extract_text_from_document(
    project_id: str, location: str, processor_id: str, file_path: str
) -> str:
    """
    Extracts plain text from a document using Google Document AI.
    """
    client = get_documentai_client()

    # The full resource name of the processor
    # e.g., projects/project_id/locations/location/processors/processor_id
    name = client.processor_path(project_id, location, processor_id)

    with open(file_path, "rb") as image:
        image_content = image.read()

    raw_document = documentai.RawDocument(
        content=image_content, mime_type="application/pdf"
    )  # Assuming PDF for simplicity

    request = documentai.ProcessRequest(name=name, raw_document=raw_document)
    result = client.process_document(request=request)
    document = result.document

    return document.text
