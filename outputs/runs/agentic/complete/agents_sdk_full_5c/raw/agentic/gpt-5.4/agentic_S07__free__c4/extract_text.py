from __future__ import annotations

from document_client import process_document_bytes
from document_models import TextExtractionResult


DEFAULT_MIME_TYPE = "image/png"


def extract_text(file_path: str, mime_type: str = DEFAULT_MIME_TYPE) -> TextExtractionResult:
    with open(file_path, "rb") as f:
        result = process_document_bytes(f.read(), mime_type)
    document = result.document
    pages = [{"page_number": page.page_number} for page in document.pages]
    return TextExtractionResult(text=document.text or "", pages=pages, provider="google_document_ai")
