from __future__ import annotations

from document_client import StructuredDocumentClient
from document_models import DocumentExtractionRequest


RECEIPT_MODEL_ID = "prebuilt-receipt"


def extract_receipt_fields(document_uri: str):
    client = StructuredDocumentClient()
    request = DocumentExtractionRequest(document_uri=document_uri, metadata={"model_id": RECEIPT_MODEL_ID})
    return client.analyze_receipt(request)
