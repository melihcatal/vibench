from __future__ import annotations

from typing import Any, Dict, List

from document_models import StructuredDocumentResponse


def validate_document_fields(extracted: StructuredDocumentResponse) -> Dict[str, Any]:
    required = ["vendor_name", "invoice_receipt_date", "total"]
    missing: List[str] = [key for key in required if key not in extracted.fields or extracted.fields[key].value in (None, "")]
    low_confidence: List[str] = []
    for key, field in extracted.fields.items():
        if field.confidence is not None and field.confidence < 0.7:
            low_confidence.append(key)
    return {
        "valid": not missing,
        "missing": missing,
        "low_confidence": low_confidence,
        "provider": "Amazon Textract AnalyzeExpense",
    }
