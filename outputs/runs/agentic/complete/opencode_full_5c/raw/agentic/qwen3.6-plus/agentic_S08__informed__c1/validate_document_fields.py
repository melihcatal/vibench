from document_models import (
    InvoiceFields,
    ReceiptFields,
    ValidationError,
    ValidationResult,
)

REQUIRED_INVOICE_FIELDS = ["vendor_name", "invoice_number", "invoice_date", "total"]
REQUIRED_RECEIPT_FIELDS = ["merchant_name", "receipt_date", "total"]
MIN_CONFIDENCE_THRESHOLD = 0.5


def validate_document_fields(
    fields: object,
    document_type: str = "invoice",
    confidence_threshold: float = MIN_CONFIDENCE_THRESHOLD,
) -> ValidationResult:
    errors = []
    confidence_warnings = []

    if document_type == "invoice":
        if not isinstance(fields, InvoiceFields):
            return ValidationResult(
                is_valid=False,
                errors=[
                    ValidationError(
                        field="_type",
                        message=f"Expected InvoiceFields, got {type(fields).__name__}",
                    )
                ],
            )
        required = REQUIRED_INVOICE_FIELDS
        field_confidences = fields.field_confidences
    elif document_type == "receipt":
        if not isinstance(fields, ReceiptFields):
            return ValidationResult(
                is_valid=False,
                errors=[
                    ValidationError(
                        field="_type",
                        message=f"Expected ReceiptFields, got {type(fields).__name__}",
                    )
                ],
            )
        required = REQUIRED_RECEIPT_FIELDS
        field_confidences = fields.field_confidences
    else:
        return ValidationResult(
            is_valid=False,
            errors=[
                ValidationError(
                    field="_type",
                    message=f"Unsupported document type: {document_type}",
                )
            ],
        )

    for field_name in required:
        value = getattr(fields, field_name, None)
        if value is None or (isinstance(value, str) and not value.strip()):
            errors.append(
                ValidationError(
                    field=field_name,
                    message=f"Required field '{field_name}' is missing or empty",
                    is_critical=True,
                )
            )

    if fields.total <= 0:
        errors.append(
            ValidationError(
                field="total",
                message="Total amount must be positive",
                is_critical=True,
            )
        )

    if fields.raw_confidence < confidence_threshold:
        confidence_warnings.append(
            f"Overall document confidence {fields.raw_confidence:.2f} is below threshold {confidence_threshold}"
        )

    for field_name, conf_value in field_confidences.items():
        if conf_value < confidence_threshold:
            confidence_warnings.append(
                f"Field '{field_name}' confidence {conf_value:.2f} is below threshold {confidence_threshold}"
            )

    is_valid = len(errors) == 0

    return ValidationResult(
        is_valid=is_valid,
        errors=errors,
        confidence_warnings=confidence_warnings,
    )


if __name__ == "__main__":
    from document_models import InvoiceFields

    sample = InvoiceFields(
        vendor_name="Test Vendor",
        invoice_number="INV-001",
        invoice_date="2024-01-01",
        total=50.0,
        raw_confidence=0.85,
        field_confidences={"supplier_name": 0.9, "invoice_number": 0.95, "date": 0.88},
    )

    result = validate_document_fields(sample, "invoice")
    print(f"Valid: {result.is_valid}")
    print(f"Errors: {result.errors}")
    print(f"Warnings: {result.confidence_warnings}")
