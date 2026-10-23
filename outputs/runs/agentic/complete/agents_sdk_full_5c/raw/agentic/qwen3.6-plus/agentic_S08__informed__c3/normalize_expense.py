"""Normalize extracted expense fields into a standard JSON schema."""

import os
import json
from datetime import datetime
from azure.ai.documentintelligence import DocumentIntelligenceClient
from azure.core.credentials import AzureKeyCredential
from document_models import (
    NormalizedExpense,
    StandardExpenseSchema,
    NormalizedLineItem,
    ExpenseSource,
    normalize_currency_amount,
    parse_date_to_iso,
)
from document_client import get_document_intelligence_client


def normalize_expense(extracted_data: dict, source: str = "invoice") -> NormalizedExpense:
    """Normalize extracted expense fields into the StandardExpenseSchema.

    Uses Azure Document Intelligence prebuilt-invoice model context to interpret fields.
    Maps vendor/receipt data into a unified expense record.
    """
    source_type = ExpenseSource.INVOICE if source == "invoice" else ExpenseSource.RECEIPT

    vendor_name = ""
    if source == "invoice":
        vendor_name = extracted_data.get("vendor_name", "") or extracted_data.get("VendorName", "")
    else:
        vendor_name = extracted_data.get("merchant_name", "") or extracted_data.get("MerchantName", "")

    raw_date = ""
    if source == "invoice":
        raw_date = extracted_data.get("invoice_date", "") or extracted_data.get("InvoiceDate", "")
    else:
        raw_date = extracted_data.get("transaction_date", "") or extracted_data.get("TransactionDate", "")

    date_iso = parse_date_to_iso(raw_date)

    total_amount = float(
        extracted_data.get("total_amount", 0.0)
        or extracted_data.get("InvoiceTotal", 0.0)
        or extracted_data.get("Total", 0.0)
    )

    tax_amount = float(
        extracted_data.get("tax_amount", 0.0)
        or extracted_data.get("TotalTax", 0.0)
        or extracted_data.get("tax", 0.0)
    )

    currency = extracted_data.get("currency", "USD")
    total_normalized = normalize_currency_amount(total_amount, currency)
    tax_normalized = normalize_currency_amount(tax_amount, currency)

    raw_items = (
        extracted_data.get("line_items", [])
        or extracted_data.get("items", [])
        or []
    )

    line_items = []
    for item in raw_items:
        desc = item.get("description", item.get("Description", ""))
        qty = float(item.get("quantity", item.get("Quantity", 0.0)))
        up = float(item.get("unit_price", item.get("UnitPrice", item.get("Price", 0.0))))
        amt = float(item.get("amount", item.get("Amount", item.get("TotalPrice", 0.0))))
        line_items.append(NormalizedLineItem(
            description=desc,
            quantity=qty,
            unit_price=normalize_currency_amount(up, currency),
            amount=normalize_currency_amount(amt, currency),
        ))

    confidence = float(extracted_data.get("confidence", 0.0))

    standard = StandardExpenseSchema(
        vendor=vendor_name,
        date=date_iso,
        total=total_normalized,
        tax=tax_normalized,
        currency=currency,
        line_items=[li.model_dump() for li in line_items],
        source=source_type.value,
        confidence=confidence,
        raw_fields=extracted_data.get("raw_fields", {}),
    )

    normalized = NormalizedExpense(
        standard_schema=standard,
        source_type=source_type,
        normalized_at=datetime.utcnow().isoformat() + "Z",
    )

    return normalized


def normalize_expense_from_file(document_path: str, source: str = "invoice") -> NormalizedExpense:
    """Extract and normalize expense from a document file in one step."""
    if source == "invoice":
        from extract_invoice_fields import extract_invoice_fields
        extracted = extract_invoice_fields(document_path)
        extracted_data = {
            "vendor_name": extracted.vendor_name,
            "invoice_date": extracted.invoice_date,
            "total_amount": extracted.total_amount,
            "line_items": [li.model_dump() for li in extracted.line_items],
            "confidence": extracted.confidence,
            "raw_fields": extracted.raw_fields,
        }
    else:
        from extract_receipt_fields import extract_receipt_fields
        extracted = extract_receipt_fields(document_path)
        extracted_data = {
            "merchant_name": extracted.merchant_name,
            "transaction_date": "",
            "total_amount": extracted.total_amount,
            "tax_amount": extracted.tax_amount,
            "items": [it.model_dump() for it in extracted.items],
            "confidence": extracted.confidence,
            "raw_fields": extracted.raw_fields,
        }

    return normalize_expense(extracted_data, source=source)


if __name__ == "__main__":
    import sys
    doc_path = sys.argv[1] if len(sys.argv) > 1 else None
    src = sys.argv[2] if len(sys.argv) > 2 else "invoice"
    if doc_path:
        result = normalize_expense_from_file(doc_path, source=src)
        print(json.dumps(result.model_dump(), indent=2))
