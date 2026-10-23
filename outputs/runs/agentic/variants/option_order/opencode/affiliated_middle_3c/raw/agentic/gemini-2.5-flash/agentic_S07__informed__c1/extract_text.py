import os
from google.cloud import documentai_v1beta3 as documentai
from document_client import DocumentAIClient
from document_models import DocumentText


def extract_text_from_document_ai(
    project_id: str,
    location: str,
    processor_id: str,
    file_content: bytes,
    mime_type: str,
) -> DocumentText:
    client = DocumentAIClient().client
    name = client.processor_path(project_id, location, processor_id)

    document = documentai.RawDocument(content=file_content, mime_type=mime_type)
    request = documentai.ProcessRequest(name=name, raw_document=document)

    result = client.process_document(request=request)
    document_response = result.document

    return DocumentText(text=document_response.text)
