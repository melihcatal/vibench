import os
from typing import Optional
from google.cloud import documentai_v1 as documentai
from document_client import get_documentai_client, get_processor_name
from document_models import DocumentInput, DocumentOutput


def extract_text_from_document(
    document_input: DocumentInput, project_id: str, location: str, processor_id: str
) -> DocumentOutput:
    """Extracts plain text from a document using Google Document AI."""
    client = get_documentai_client()
    processor_name = get_processor_name(project_id, location, processor_id)

    # The Document AI AIPlatform-hosted service has a specific client.
    # The standard Document AI client (used here) handles various processors including OCR.

    raw_document = documentai.RawDocument(
        content=document_input.content,
        mime_type=document_input.mime_type,
    )

    request = documentai.ProcessRequest(
        name=processor_name,
        raw_document=raw_document,
    )

    response = client.process_document(request=request)
    document = response.document

    return DocumentOutput(text=document.text)
