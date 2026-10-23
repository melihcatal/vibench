from __future__ import annotations

from typing import Any, Dict

from document_models import ExtractionResult, LineItem, standard_expense_schema


def normalize_expense(extracted_fields: Dict[str, Any]) -> Dict[str, Any]:
    extraction = ExtractionResult(
        document_type=extracted_fields.get("document_type", "expense"),
        vendor=extracted_fields.get("vendor"),
        merchant=extracted_fields.get("merchant"),
        invoice_date=extracted_fields.get("invoice_date"),
        total=extracted_fields.get("total"),
        tax=extracted_fields.get("tax"),
        currency=extracted_fields.get("currency"),
        notes=extracted_fields.get("notes"),
        line_items=[
            LineItem(**item) for item in extracted_fields.get("line_items", [])
        ],
        confidence_scores=extracted_fields.get("confidence_scores", {}),
        raw_response=extracted_fields.get("raw_response", {}),
    )
    normalized = standard_expense_schema(extraction)
    normalized["provider"] = {
        "name": "azure-document-intelligence",
        "model_id": "prebuilt-invoice"
        if extraction.document_type == "invoice"
        else "prebuilt-receipt",
    }
    return normalized
