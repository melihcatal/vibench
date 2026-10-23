from document_models import (
    ExtractedField,
    InvoiceExtraction,
    NormalizedExpense,
    ReceiptExtraction,
    ValidationResult,
)

INVOICE_REQUIRED_FIELDS = ["vendor_name", "invoice_date", "invoice_total"]
RECEIPT_REQUIRED_FIELDS = ["merchant_name", "receipt_total"]
EXPENSE_REQUIRED_FIELDS = [
    "document_type",
    "vendor_or_merchant",
    "document_date",
    "total",
]
DEFAULT_CONFIDENCE_THRESHOLD = 0.5


def validate_invoice_fields(
    invoice: InvoiceExtraction,
    confidence_threshold: float = DEFAULT_CONFIDENCE_THRESHOLD,
) -> ValidationResult:
    missing = []
    low_confidence = []
    for field_name in INVOICE_REQUIRED_FIELDS:
        field_obj = getattr(invoice, field_name, None)
        if field_obj is None or (
            isinstance(field_obj, ExtractedField)
            and field_obj.value in (None, "", 0, 0.0)
        ):
            missing.append(field_name)
        elif (
            isinstance(field_obj, ExtractedField)
            and field_obj.confidence < confidence_threshold
        ):
            low_confidence.append(field_name)
    for i, item in enumerate(invoice.line_items):
        if not item.description.value:
            missing.append(f"line_items[{i}].description")
    is_valid = len(missing) == 0 and len(low_confidence) == 0
    return ValidationResult(
        is_valid=is_valid,
        missing_fields=missing,
        low_confidence_fields=low_confidence,
        confidence_threshold=confidence_threshold,
        details={"document_type": "invoice"},
    )


def validate_receipt_fields(
    receipt: ReceiptExtraction,
    confidence_threshold: float = DEFAULT_CONFIDENCE_THRESHOLD,
) -> ValidationResult:
    missing = []
    low_confidence = []
    for field_name in RECEIPT_REQUIRED_FIELDS:
        field_obj = getattr(receipt, field_name, None)
        if field_obj is None or (
            isinstance(field_obj, ExtractedField)
            and field_obj.value in (None, "", 0, 0.0)
        ):
            missing.append(field_name)
        elif (
            isinstance(field_obj, ExtractedField)
            and field_obj.confidence < confidence_threshold
        ):
            low_confidence.append(field_name)
    for i, item in enumerate(receipt.items):
        if not item.description.value:
            missing.append(f"items[{i}].description")
    is_valid = len(missing) == 0 and len(low_confidence) == 0
    return ValidationResult(
        is_valid=is_valid,
        missing_fields=missing,
        low_confidence_fields=low_confidence,
        confidence_threshold=confidence_threshold,
        details={"document_type": "receipt"},
    )


def validate_expense_fields(
    expense: NormalizedExpense,
    confidence_threshold: float = DEFAULT_CONFIDENCE_THRESHOLD,
) -> ValidationResult:
    missing = []
    low_confidence = []
    for field_name in EXPENSE_REQUIRED_FIELDS:
        value = getattr(expense, field_name, None)
        if value is None or value in ("", 0, 0.0):
            missing.append(field_name)
    if expense.extraction_confidence < confidence_threshold:
        low_confidence.append("extraction_confidence")
    is_valid = len(missing) == 0 and len(low_confidence) == 0
    return ValidationResult(
        is_valid=is_valid,
        missing_fields=missing,
        low_confidence_fields=low_confidence,
        confidence_threshold=confidence_threshold,
        details={"document_type": expense.document_type},
    )


def validate_document_fields(
    extraction, confidence_threshold: float = DEFAULT_CONFIDENCE_THRESHOLD
) -> ValidationResult:
    if isinstance(extraction, InvoiceExtraction):
        return validate_invoice_fields(extraction, confidence_threshold)
    elif isinstance(extraction, ReceiptExtraction):
        return validate_receipt_fields(extraction, confidence_threshold)
    elif isinstance(extraction, NormalizedExpense):
        return validate_expense_fields(extraction, confidence_threshold)
    else:
        raise TypeError(f"Unsupported extraction type: {type(extraction)}")
