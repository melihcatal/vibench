from document_models import (
    InvoiceExtractionResult,
    ReceiptExtractionResult,
    NormalizedExpenseRecord,
    normalize_invoice_to_expense,
    normalize_receipt_to_expense,
)


def normalize_expense_from_invoice(
    invoice_result: InvoiceExtractionResult,
) -> NormalizedExpenseRecord:
    return normalize_invoice_to_expense(invoice_result)


def normalize_expense_from_receipt(
    receipt_result: ReceiptExtractionResult,
) -> NormalizedExpenseRecord:
    return normalize_receipt_to_expense(receipt_result)


def normalize_expense_from_dict(
    extraction_data: dict, source_type: str
) -> NormalizedExpenseRecord:
    if source_type == "invoice":
        invoice_result = InvoiceExtractionResult(
            vendor_name=extraction_data.get("vendor_name", {}),
            invoice_date=extraction_data.get("invoice_date", {}),
            invoice_total=extraction_data.get("invoice_total", {}),
            invoice_sub_total=extraction_data.get("invoice_sub_total", {}),
            invoice_tax=extraction_data.get("invoice_tax", {}),
            invoice_id=extraction_data.get("invoice_id", {}),
            billing_address=extraction_data.get("billing_address", {}),
            raw_fields=extraction_data.get("raw_fields", {}),
        )
        return normalize_invoice_to_expense(invoice_result)
    elif source_type == "receipt":
        receipt_result = ReceiptExtractionResult(
            merchant_name=extraction_data.get("merchant_name", {}),
            transaction_date=extraction_data.get("transaction_date", {}),
            transaction_total=extraction_data.get("transaction_total", {}),
            tax=extraction_data.get("tax", {}),
            subtotal=extraction_data.get("subtotal", {}),
            receipt_id=extraction_data.get("receipt_id", {}),
            raw_fields=extraction_data.get("raw_fields", {}),
        )
        return normalize_receipt_to_expense(receipt_result)
    else:
        raise ValueError(f"Unsupported source_type: {source_type}")


def batch_normalize_expenses(extractions: list) -> list:
    normalized = []
    for extraction in extractions:
        source_type = extraction.get("source_type", "")
        data = extraction.get("data", {})
        record = normalize_expense_from_dict(data, source_type)
        normalized.append(record)
    return normalized
