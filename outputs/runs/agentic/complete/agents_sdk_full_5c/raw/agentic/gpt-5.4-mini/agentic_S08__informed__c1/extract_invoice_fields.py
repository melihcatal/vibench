from __future__ import annotations

from document_client import StructuredDocumentClient
from document_models import DocumentExtractionRequest


INVOICE_MODEL_ID = "prebuilt-invoice"


def extract_invoice_fields(document_uri: str):
    client = StructuredDocumentClient()
    request = DocumentExtractionRequest(document_uri=document_uri, metadata={"model_id": INVOICE_MODEL_ID})
    return client.analyze_invoice(request)
