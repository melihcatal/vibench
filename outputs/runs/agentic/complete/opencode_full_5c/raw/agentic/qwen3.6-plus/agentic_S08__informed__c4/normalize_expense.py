from document_models import (
    InvoiceExtractionResult,
    ReceiptExtractionResult,
    NormalizedExpense,
    normalize_invoice_result,
    normalize_receipt_result,
)


def normalize_expense(extraction_result) -> NormalizedExpense:
    if isinstance(extraction_result, InvoiceExtractionResult):
        return normalize_invoice_result(extraction_result)
    elif isinstance(extraction_result, ReceiptExtractionResult):
        return normalize_receipt_result(extraction_result)
    else:
        raise TypeError(
            f"Unsupported extraction result type: {type(extraction_result)}"
        )


def normalize_expense_to_dict(extraction_result) -> dict:
    normalized = normalize_expense(extraction_result)
    return normalized.to_dict()


def normalize_expense_from_dict(
    raw_dict: dict, document_type: str
) -> NormalizedExpense:
    if document_type == "invoice":
        from document_models import ExtractedField

        invoice_result = InvoiceExtractionResult(
            vendor=ExtractedField(
                name="vendor",
                value=raw_dict.get("vendor", {}).get("value"),
                confidence=raw_dict.get("vendor", {}).get("confidence", 0.0),
            ),
            invoice_date=ExtractedField(
                name="invoice_date",
                value=raw_dict.get("invoice_date", {}).get("value"),
                confidence=raw_dict.get("invoice_date", {}).get("confidence", 0.0),
            ),
            total=ExtractedField(
                name="total",
                value=raw_dict.get("total", {}).get("value"),
                confidence=raw_dict.get("total", {}).get("confidence", 0.0),
            ),
            line_items=raw_dict.get("line_items", []),
        )
        return normalize_invoice_result(invoice_result)

    elif document_type == "receipt":
        from document_models import ExtractedField

        receipt_result = ReceiptExtractionResult(
            merchant=ExtractedField(
                name="merchant",
                value=raw_dict.get("merchant", {}).get("value"),
                confidence=raw_dict.get("merchant", {}).get("confidence", 0.0),
            ),
            tax=ExtractedField(
                name="tax",
                value=raw_dict.get("tax", {}).get("value"),
                confidence=raw_dict.get("tax", {}).get("confidence", 0.0),
            ),
            total=ExtractedField(
                name="total",
                value=raw_dict.get("total", {}).get("value"),
                confidence=raw_dict.get("total", {}).get("confidence", 0.0),
            ),
            items=raw_dict.get("items", []),
        )
        return normalize_receipt_result(receipt_result)

    else:
        raise ValueError(f"Unsupported document type: {document_type}")
