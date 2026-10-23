import os
from google.cloud import documentai_v1 as documentai
from document_client import get_documentai_client


def extract_text_from_document(
    project_id: str,
    location: str,
    processor_id: str,
    file_content: bytes,
    mime_type: str,
) -> str:
    """Extracts plain text from a document using Google Document AI."""
    client = get_documentai_client()
    processor_name = client.processor_path(project_id, location, processor_id)

    raw_document = documentai.RawDocument(content=file_content, mime_type=mime_type)
    request = documentai.ProcessRequest(name=processor_name, raw_document=raw_document)

    response = client.process_document(request=request)
    document = response.document

    return document.text
