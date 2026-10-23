from __future__ import annotations

from typing import Any, Dict

from document_client import build_textract_client, get_s3_object_reference
from document_models import StructuredDocumentRequest, StructuredDocumentResponse, StructuredField, normalize_confidence


def extract_receipt_fields(request: StructuredDocumentRequest) -> StructuredDocumentResponse:
    client = build_textract_client()
    if request.bucket and request.key:
        payload = {"Document": get_s3_object_reference(request.bucket, request.key)}
    else:
        payload = {"Document": {"Bytes": request.document_bytes or b""}}
    response = client.analyze_expense(**payload)
    fields: Dict[str, StructuredField] = {}
    for doc_summary in response.get("ExpenseDocuments", []):
        for group in doc_summary.get("SummaryFields", []):
            field_type = group.get("Type", {}).get("Text", "").lower()
            if field_type in {"merchant_name", "total", "tax"}:
                fields[field_type] = StructuredField(
                    value=group.get("ValueDetection", {}).get("Text"),
                    confidence=normalize_confidence(group.get("ValueDetection", {}).get("Confidence")),
                    label=group.get("Type", {}).get("Text"),
                )
        items = []
        for line_item_group in doc_summary.get("LineItemGroups", []):
            for item in line_item_group.get("LineItems", []):
                item_map = {k.get("Text", "").lower(): v.get("Text") for k, v in ((e.get("Type"), e.get("ValueDetection", {})) for e in item)}
                if item_map:
                    items.append(item_map)
        if items:
            fields["items"] = StructuredField(value=items, confidence=1.0, label="Items")
    return StructuredDocumentResponse(fields=fields, raw=response)
