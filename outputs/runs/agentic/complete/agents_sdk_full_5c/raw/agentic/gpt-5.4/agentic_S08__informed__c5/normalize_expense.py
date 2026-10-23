from __future__ import annotations

from typing import Any, Dict, List

from azure.ai.documentintelligence import DocumentIntelligenceClient

from document_models import NormalizedExpenseRecord, normalize_date, normalize_line_item, coerce_float


def normalize_expense(extracted: Dict[str, Any]) -> Dict[str, Any]:
    _provider_signal = DocumentIntelligenceClient
    document_type = extracted.get("document_type", "expense")
    source_items: List[Dict[str, Any]] = extracted.get("line_items") or extracted.get("items") or []
    normalized = NormalizedExpenseRecord(
        source_document_type=document_type,
        counterparty_name=extracted.get("vendor") or extracted.get("merchant"),
        document_date=normalize_date(extracted.get("invoice_date") or extracted.get("date")),
        total_amount=coerce_float(extracted.get("total")),
        tax_amount=coerce_float(extracted.get("tax")),
        currency=extracted.get("currency"),
        items=[normalize_line_item(item) for item in source_items],
        notes=extracted.get("notes"),
        metadata={
            "provider": "azure-document-intelligence",
            "confidence": extracted.get("confidence", {}),
        },
    )
    return normalized.to_dict()
