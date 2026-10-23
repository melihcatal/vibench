from document_models import (
    InvoiceExtractionResult,
    ReceiptExtractionResult,
    NormalizedExpenseRecord,
)


INVOICE_REQUIRED_FIELDS = ["vendor_name", "invoice_date", "invoice_total"]
RECEIPT_REQUIRED_FIELDS = ["merchant_name", "transaction_date", "transaction_total"]
MINIMUM_CONFIDENCE_THRESHOLD = 0.5


class FieldValidationError(Exception):
    def __init__(self, field_name, message, confidence=None):
        self.field_name = field_name
        self.message = message
        self.confidence = confidence
        super().__init__(self.message)


class ValidationReport:
    def __init__(self):
        self.is_valid = True
        self.errors = []
        self.warnings = []
        self.overall_confidence = 0.0

    def add_error(self, field_name, message, confidence=None):
        self.is_valid = False
        self.errors.append(
            {
                "field": field_name,
                "message": message,
                "confidence": confidence,
            }
        )

    def add_warning(self, field_name, message, confidence=None):
        self.warnings.append(
            {
                "field": field_name,
                "message": message,
                "confidence": confidence,
            }
        )

    def to_dict(self):
        return {
            "is_valid": self.is_valid,
            "errors": self.errors,
            "warnings": self.warnings,
            "overall_confidence": self.overall_confidence,
        }


def validate_invoice_fields(
    invoice_result: InvoiceExtractionResult, min_confidence=MINIMUM_CONFIDENCE_THRESHOLD
) -> ValidationReport:
    report = ValidationReport()

    for field_name in INVOICE_REQUIRED_FIELDS:
        field_obj = getattr(invoice_result, field_name, None)
        if field_obj is None:
            report.add_error(field_name, f"Required field '{field_name}' is missing")
            continue

        value = field_obj.value if hasattr(field_obj, "value") else field_obj
        confidence = field_obj.confidence if hasattr(field_obj, "confidence") else 0.0

        if value is None or (isinstance(value, str) and not value.strip()):
            report.add_error(
                field_name, f"Required field '{field_name}' is empty", confidence
            )
        elif confidence < min_confidence:
            report.add_warning(
                field_name,
                f"Field '{field_name}' has low confidence ({confidence:.2f})",
                confidence,
            )

    if invoice_result.line_items:
        for idx, item in enumerate(invoice_result.line_items):
            if not item.description:
                report.add_warning(
                    f"line_items[{idx}]",
                    "Line item missing description",
                    item.confidence,
                )
            if item.amount <= 0:
                report.add_warning(
                    f"line_items[{idx}]",
                    "Line item amount is zero or negative",
                    item.confidence,
                )

    confidences = [
        invoice_result.vendor_name.confidence,
        invoice_result.invoice_date.confidence,
        invoice_result.invoice_total.confidence,
    ]
    valid_confidences = [c for c in confidences if c > 0]
    report.overall_confidence = (
        round(sum(valid_confidences) / len(valid_confidences), 4)
        if valid_confidences
        else 0.0
    )

    return report


def validate_receipt_fields(
    receipt_result: ReceiptExtractionResult, min_confidence=MINIMUM_CONFIDENCE_THRESHOLD
) -> ValidationReport:
    report = ValidationReport()

    for field_name in RECEIPT_REQUIRED_FIELDS:
        field_obj = getattr(receipt_result, field_name, None)
        if field_obj is None:
            report.add_error(field_name, f"Required field '{field_name}' is missing")
            continue

        value = field_obj.value if hasattr(field_obj, "value") else field_obj
        confidence = field_obj.confidence if hasattr(field_obj, "confidence") else 0.0

        if value is None or (isinstance(value, str) and not value.strip()):
            report.add_error(
                field_name, f"Required field '{field_name}' is empty", confidence
            )
        elif confidence < min_confidence:
            report.add_warning(
                field_name,
                f"Field '{field_name}' has low confidence ({confidence:.2f})",
                confidence,
            )

    if receipt_result.items:
        for idx, item in enumerate(receipt_result.items):
            if not item.description:
                report.add_warning(
                    f"items[{idx}]", "Receipt item missing description", item.confidence
                )
            if item.amount <= 0:
                report.add_warning(
                    f"items[{idx}]",
                    "Receipt item amount is zero or negative",
                    item.confidence,
                )

    confidences = [
        receipt_result.merchant_name.confidence,
        receipt_result.transaction_date.confidence,
        receipt_result.transaction_total.confidence,
    ]
    valid_confidences = [c for c in confidences if c > 0]
    report.overall_confidence = (
        round(sum(valid_confidences) / len(valid_confidences), 4)
        if valid_confidences
        else 0.0
    )

    return report


def validate_normalized_expense(
    expense_record: NormalizedExpenseRecord, min_confidence=MINIMUM_CONFIDENCE_THRESHOLD
) -> ValidationReport:
    report = ValidationReport()

    if not expense_record.vendor_or_merchant:
        report.add_error("vendor_or_merchant", "Vendor/merchant name is missing")
    if not expense_record.document_date:
        report.add_error("document_date", "Document date is missing")
    if expense_record.total_amount <= 0:
        report.add_error("total_amount", "Total amount must be positive")
    if expense_record.confidence_overall < min_confidence:
        report.add_warning(
            "confidence_overall",
            f"Overall confidence below threshold ({expense_record.confidence_overall:.2f})",
            expense_record.confidence_overall,
        )

    report.overall_confidence = expense_record.confidence_overall
    return report
