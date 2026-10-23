from __future__ import annotations

from document_client import extract_text_spans, process_document
from document_models import DocumentRequest, OCRTextResult


def extract_text(request: DocumentRequest) -> OCRTextResult:
    document = process_document(request, "GOOGLE_DOCUMENTAI_OCR_PROCESSOR_ID")
    return extract_text_spans(document)
