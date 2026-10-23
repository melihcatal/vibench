import json
from datetime import datetime
from typing import Dict, List, Any, Optional
from document_models import (
    NormalizedExpense,
    InvoiceExtraction,
    ReceiptExtraction,
    create_expense_id,
)


def normalize_invoice_expense(
    invoice: InvoiceExtraction, currency: str = "USD"
) -> NormalizedExpense:
    vendor = (
        str(invoice.vendor_name.value)
        if invoice.vendor_name.value
        else "Unknown Vendor"
    )

    date_str = str(invoice.invoice_date.value) if invoice.invoice_date.value else None
    try:
        if date_str:
            date_obj = datetime.strptime(date_str, "%Y-%m-%d")
        else:
            date_obj = datetime.now()
    except (ValueError, TypeError):
        date_obj = datetime.now()

    total = 0.0
    try:
        total = (
            float(invoice.invoice_total.value) if invoice.invoice_total.value else 0.0
        )
    except (ValueError, TypeError):
        total = 0.0

    line_items = []
    for item in invoice.line_items:
        line_items.append(
            {
                "description": item.description,
                "quantity": item.quantity,
                "unit_price": item.unit_price,
                "total": item.total_price,
                "confidence": item.confidence,
            }
        )

    confidence_score = calculate_overall_confidence(invoice)
    expense_id = create_expense_id(vendor, date_obj, total)

    metadata = {
        "source_type": "invoice",
        "extraction_confidence": confidence_score,
        "vendor_confidence": invoice.vendor_name.confidence,
        "date_confidence": invoice.invoice_date.confidence,
        "total_confidence": invoice.invoice_total.confidence,
    }

    return NormalizedExpense(
        expense_id=expense_id,
        vendor=vendor,
        date=date_obj,
        total_amount=total,
        currency=currency,
        line_items=line_items,
        metadata=metadata,
        confidence_score=confidence_score,
    )


def normalize_receipt_expense(
    receipt: ReceiptExtraction, currency: str = "USD"
) -> NormalizedExpense:
    vendor = (
        str(receipt.merchant_name.value)
        if receipt.merchant_name.value
        else "Unknown Merchant"
    )

    date_str = (
        str(receipt.transaction_date.value) if receipt.transaction_date.value else None
    )
    try:
        if date_str:
            date_obj = datetime.strptime(date_str, "%Y-%m-%d")
        else:
            date_obj = datetime.now()
    except (ValueError, TypeError):
        date_obj = datetime.now()

    total = 0.0
    try:
        total = float(receipt.total_amount.value) if receipt.total_amount.value else 0.0
    except (ValueError, TypeError):
        total = 0.0

    line_items = []
    for item in receipt.items:
        line_items.append(
            {
                "description": item.description,
                "quantity": item.quantity,
                "unit_price": item.unit_price,
                "total": item.total_price,
                "confidence": item.confidence,
            }
        )

    confidence_score = calculate_overall_confidence_receipt(receipt)
    expense_id = create_expense_id(vendor, date_obj, total)

    metadata = {
        "source_type": "receipt",
        "extraction_confidence": confidence_score,
        "merchant_confidence": receipt.merchant_name.confidence,
        "date_confidence": receipt.transaction_date.confidence,
        "total_confidence": receipt.total_amount.confidence,
        "tax_confidence": receipt.tax_amount.confidence,
    }

    return NormalizedExpense(
        expense_id=expense_id,
        vendor=vendor,
        date=date_obj,
        total_amount=total,
        currency=currency,
        line_items=line_items,
        metadata=metadata,
        confidence_score=confidence_score,
    )


def calculate_overall_confidence(invoice: InvoiceExtraction) -> float:
    confidences = [
        invoice.vendor_name.confidence,
        invoice.invoice_date.confidence,
        invoice.invoice_total.confidence,
    ]
    if invoice.line_items:
        item_confidences = [item.confidence for item in invoice.line_items]
        confidences.extend(item_confidences)

    return sum(confidences) / len(confidences) if confidences else 0.0


def calculate_overall_confidence_receipt(receipt: ReceiptExtraction) -> float:
    confidences = [
        receipt.merchant_name.confidence,
        receipt.transaction_date.confidence,
        receipt.tax_amount.confidence,
        receipt.total_amount.confidence,
    ]
    if receipt.items:
        item_confidences = [item.confidence for item in receipt.items]
        confidences.extend(item_confidences)

    return sum(confidences) / len(confidences) if confidences else 0.0


def expense_to_json(expense: NormalizedExpense) -> str:
    data = {
        "expense_id": expense.expense_id,
        "vendor": expense.vendor,
        "date": expense.date.isoformat(),
        "total_amount": expense.total_amount,
        "currency": expense.currency,
        "line_items": expense.line_items,
        "metadata": expense.metadata,
        "confidence_score": expense.confidence_score,
    }
    return json.dumps(data, indent=2, default=str)
