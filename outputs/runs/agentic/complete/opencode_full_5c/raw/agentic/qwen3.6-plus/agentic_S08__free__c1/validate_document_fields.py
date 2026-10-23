from typing import Dict, Any, List, Union

from document_models import (
    InvoiceExtraction,
    ReceiptExtraction,
    NormalizedExpense,
    ValidationResult,
)


REQUIRED_INVOICE_FIELDS = [
    "vendor",
    "invoice_date",
    "total_amount",
]

REQUIRED_RECEIPT_FIELDS = [
    "merchant",
    "receipt_date",
    "total_amount",
]

REQUIRED_NORMALIZED_FIELDS = [
    "document_type",
    "vendor_or_merchant",
    "transaction_date",
    "total_amount",
    "currency",
]

DEFAULT_CONFIDENCE_THRESHOLD = 0.7


def validate_document_fields(
    extraction: Union[InvoiceExtraction, ReceiptExtraction, NormalizedExpense],
    confidence_threshold: float = DEFAULT_CONFIDENCE_THRESHOLD,
) -> ValidationResult:
    if isinstance(extraction, InvoiceExtraction):
        return _validate_invoice(extraction, confidence_threshold)
    elif isinstance(extraction, ReceiptExtraction):
        return _validate_receipt(extraction, confidence_threshold)
    elif isinstance(extraction, NormalizedExpense):
        return _validate_normalized(extraction, confidence_threshold)
    else:
        raise TypeError(f"Unsupported extraction type: {type(extraction).__name__}")


def _validate_invoice(
    extraction: InvoiceExtraction, confidence_threshold: float
) -> ValidationResult:
    missing = []
    low_confidence = []
    details = {}

    for field_name in REQUIRED_INVOICE_FIELDS:
        value = getattr(extraction, field_name, None)
        if not value or (isinstance(value, (int, float)) and value == 0):
            missing.append(field_name)
        else:
            details[field_name] = {"value": str(value), "present": True}

    for fname, field_obj in extraction.raw_fields.items():
        if field_obj.confidence < confidence_threshold:
            low_confidence.append(fname)
        details[fname] = {
            "value": field_obj.value,
            "confidence": field_obj.confidence,
        }

    if extraction.confidence_overall < confidence_threshold:
        details["confidence_overall"] = {
            "value": extraction.confidence_overall,
            "below_threshold": True,
        }

    is_valid = len(missing) == 0 and len(low_confidence) == 0

    return ValidationResult(
        is_valid=is_valid,
        missing_fields=missing,
        low_confidence_fields=low_confidence,
        confidence_threshold=confidence_threshold,
        details=details,
    )


def _validate_receipt(
    extraction: ReceiptExtraction, confidence_threshold: float
) -> ValidationResult:
    missing = []
    low_confidence = []
    details = {}

    for field_name in REQUIRED_RECEIPT_FIELDS:
        value = getattr(extraction, field_name, None)
        if not value or (isinstance(value, (int, float)) and value == 0):
            missing.append(field_name)
        else:
            details[field_name] = {"value": str(value), "present": True}

    for fname, field_obj in extraction.raw_fields.items():
        if field_obj.confidence < confidence_threshold:
            low_confidence.append(fname)
        details[fname] = {
            "value": field_obj.value,
            "confidence": field_obj.confidence,
        }

    if extraction.confidence_overall < confidence_threshold:
        details["confidence_overall"] = {
            "value": extraction.confidence_overall,
            "below_threshold": True,
        }

    is_valid = len(missing) == 0 and len(low_confidence) == 0

    return ValidationResult(
        is_valid=is_valid,
        missing_fields=missing,
        low_confidence_fields=low_confidence,
        confidence_threshold=confidence_threshold,
        details=details,
    )


def _validate_normalized(
    extraction: NormalizedExpense, confidence_threshold: float
) -> ValidationResult:
    missing = []
    low_confidence = []
    details = {}
    data = extraction.to_json()

    for field_name in REQUIRED_NORMALIZED_FIELDS:
        value = data.get(field_name)
        if not value or (isinstance(value, (int, float)) and value == 0):
            missing.append(field_name)
        else:
            details[field_name] = {"value": str(value), "present": True}

    metadata = data.get("metadata", {})
    overall_conf = metadata.get("confidence_overall", 1.0)
    if overall_conf < confidence_threshold:
        low_confidence.append("confidence_overall")
        details["confidence_overall"] = {
            "value": overall_conf,
            "below_threshold": True,
        }

    is_valid = len(missing) == 0 and len(low_confidence) == 0

    return ValidationResult(
        is_valid=is_valid,
        missing_fields=missing,
        low_confidence_fields=low_confidence,
        confidence_threshold=confidence_threshold,
        details=details,
    )
