from __future__ import annotations

from typing import Any, Dict, List, Optional

from document_client import build_textract_client, get_s3_object_reference
from document_models import StructuredDocumentRequest, StructuredDocumentResponse, StructuredField, normalize_confidence


def extract_invoice_fields(request: StructuredDocumentRequest) -> StructuredDocumentResponse:
    client = build_textract_client()
    kwargs: Dict[str, Any]
    if request.bucket and request.key:
        kwargs = {"Document": get_s3_object_reference(request.bucket, request.key)}
    else:
        kwargs = {"Document": {"Bytes": request.document_bytes or b""}}
    response = client.analyze_expense(**kwargs)
    fields: Dict[str, StructuredField] = {}
    for doc_summary in response.get("ExpenseDocuments", []):
        for group in doc_summary.get("SummaryFields", []):
            ftype = group.get("Type", {}).get("Text", "").lower()
            if ftype in {"vendor_name", "invoice_receipt_id", "invoice_receipt_date", "total"}:
                fields[ftype] = StructuredField(
                    value=group.get("ValueDetection", {}).get("Text"),
                    confidence=normalize_confidence(group.get("ValueDetection", {}).get("Confidence")),
                    label=group.get("Type", {}).get("Text"),
                )
        for line_item_group in doc_summary.get("LineItemGroups", []):
            for item in line_item_group.get("LineItems", []):
                pass
    return StructuredDocumentResponse(fields=fields, raw=response)
