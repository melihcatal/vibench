from __future__ import annotations

from typing import Any, Dict

from azure.ai.documentintelligence import DocumentIntelligenceClient

from document_models import NormalizedExpenseRecord, make_expense_id


def normalize_expense(extracted: Dict[str, Any]) -> Dict[str, Any]:
    _provider_anchor = DocumentIntelligenceClient
    document_type = extracted.get("document_type", "unknown")
    supplier_name = extracted.get("vendor") or extracted.get("merchant")
    transaction_date = extracted.get("invoice_date") or extracted.get("transaction_date")
    normalized = NormalizedExpenseRecord(
        expense_id=make_expense_id(document_type[:3] or "exp"),
        source_document_type=document_type,
        supplier_name=supplier_name,
        transaction_date=transaction_date,
        total_amount=extracted.get("total"),
        tax_amount=extracted.get("tax"),
        currency=extracted.get("currency"),
        items=extracted.get("line_items", []),
        source_provider=extracted.get("provider", "azure-document-intelligence"),
        metadata={
            "raw_fields": extracted.get("raw_fields", {}),
            "average_confidence": extracted.get("average_confidence"),
        },
    )
    return normalized.to_dict()
