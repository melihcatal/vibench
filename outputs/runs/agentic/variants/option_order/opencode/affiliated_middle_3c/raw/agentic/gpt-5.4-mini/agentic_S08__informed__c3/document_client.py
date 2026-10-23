import os
import boto3
from typing import Any, Dict

from document_models import (
    DocumentRequest,
    DocumentResponse,
    normalize_fields,
    normalize_items,
)


def _textract_client():
    return boto3.client("textract")


def extract_expense(request: DocumentRequest) -> DocumentResponse:
    client = _textract_client()
    result = client.analyze_expense(Document={"Bytes": request.content})
    return DocumentResponse(provider="amazon-textract-analyzeexpense", data=result)


def _safe_float(value: Any):
    try:
        return float(value)
    except Exception:
        return None


def parse_textract_expense(result: Dict[str, Any]) -> Dict[str, Any]:
    documents = result.get("ExpenseDocuments", [])
    if not documents:
        return {}
    doc = documents[0]
    summary = {
        item.get("Type", {}).get("Text"): item.get("ValueDetection", {}).get("Text")
        for item in doc.get("SummaryFields", [])
    }
    items = []
    for line in doc.get("LineItemGroups", []):
        for line_item in line.get("LineItems", []):
            item = {
                field.get("Type", {}).get("Text"): field.get("ValueDetection", {}).get(
                    "Text"
                )
                for field in line_item.get("LineItemExpenseFields", [])
            }
            if item:
                items.append(item)
    return normalize_fields(
        {
            "vendor": summary.get("VENDOR_NAME") or summary.get("SUPPLIER_NAME"),
            "date": summary.get("INVOICE_RECEIPT_DATE"),
            "total": _safe_float(summary.get("TOTAL")),
            "tax": _safe_float(summary.get("TAX")),
            "items": normalize_items(items),
            "confidence": doc.get("Confidence"),
        }
    )
