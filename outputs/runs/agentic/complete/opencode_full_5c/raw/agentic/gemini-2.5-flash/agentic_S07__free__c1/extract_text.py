from google.cloud import documentai_v1 as documentai
from document_client import get_document_ai_client
from document_models import DocumentInput, DocumentOutput
import os


def extract_plain_text(document_input: DocumentInput) -> DocumentOutput:
    client = get_document_ai_client()
    project_id = os.environ.get("GOOGLE_CLOUD_PROJECT_ID")
    location = os.environ.get("GOOGLE_CLOUD_LOCATION", "us")
    processor_id = os.environ.get("DOCUMENT_AI_OCR_PROCESSOR_ID")

    if not processor_id:
        raise ValueError("DOCUMENT_AI_OCR_PROCESSOR_ID environment variable not set.")

    name = client.processor_path(project_id, location, processor_id)

    raw_document = documentai.RawDocument(
        content=document_input.content, mime_type=document_input.mime_type
    )

    request = documentai.ProcessRequest(name=name, raw_document=raw_document)
    result = client.process_document(request=request)

    document = result.document
    return DocumentOutput(text=document.text)
