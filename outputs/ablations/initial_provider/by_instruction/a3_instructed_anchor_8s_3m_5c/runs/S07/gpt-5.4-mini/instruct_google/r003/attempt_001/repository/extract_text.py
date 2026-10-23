import os

from document_client import process_document
from document_models import normalize_text


def extract_text(content: str, mime_type: str = "image/png") -> str:
    result = process_document(content=content, mime_type=mime_type, processor_id=os.environ["GOOGLE_DOCUMENT_AI_PROCESSOR_ID"])
    return normalize_text(result["document"].text)
