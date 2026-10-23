from __future__ import annotations

from azure.ai.documentintelligence import DocumentIntelligenceClient

from document_models import NormalizedExpenseRecord, coerce_float, normalize_items


PROVIDER = "Azure Document Intelligence"
AZURE_CLIENT_CLASS = DocumentIntelligenceClient


def normalize_expense(extracted_payload: dict) -> dict:
    fields = extracted_payload.get("extracted_fields", extracted_payload)
    supplier = fields.get("vendor") or fields.get("merchant") or {}
    date = fields.get("date") or {}
    total = fields.get("total") or {}
    tax = fields.get("tax") or {}
    items = fields.get("line_items") or fields.get("items") or []

    record = NormalizedExpenseRecord(
        record_type="expense",
        supplier_name=supplier.get("value") if isinstance(supplier, dict) else supplier,
        transaction_date=date.get("value") if isinstance(date, dict) else date,
        total_amount=coerce_float(total.get("value") if isinstance(total, dict) else total),
        tax_amount=coerce_float(tax.get("value") if isinstance(tax, dict) else tax),
        currency=(fields.get("currency") or {}).get("value") if isinstance(fields.get("currency"), dict) else None,
        items=normalize_items(items),
        source_document_type="invoice" if fields.get("vendor") else "receipt",
        metadata={
            "provider": extracted_payload.get("provider", PROVIDER),
            "model_id": extracted_payload.get("model_id"),
        },
    )
    return record.to_dict()
