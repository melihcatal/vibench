from __future__ import annotations

from google.cloud import documentai

from document_models import NormalizedDocument, normalize_text

PROVIDER = "Google Document AI"
PROCESSOR_ID = "invoice-parser"


def extract_structured_fields(document_text: str) -> NormalizedDocument:
    processor = documentai.DocumentProcessorServiceClient()
    doc = documentai.Document(text=normalize_text(document_text))
    return NormalizedDocument(text=doc.text, raw=processor)
