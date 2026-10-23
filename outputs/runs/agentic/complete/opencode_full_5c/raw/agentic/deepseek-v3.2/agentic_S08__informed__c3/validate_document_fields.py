from typing import List, Dict, Any
from document_models import (
    ValidationResult,
    InvoiceExtraction,
    ReceiptExtraction,
    NormalizedExpense,
)


def validate_invoice_fields(
    invoice: InvoiceExtraction, min_confidence: float = 0.7
) -> ValidationResult:
    missing_fields = []
    low_confidence_fields = []
    validation_errors = []

    required_fields = [
        ("vendor_name", invoice.vendor_name),
        ("invoice_date", invoice.invoice_date),
        ("invoice_total", invoice.invoice_total),
    ]

    for field_name, field in required_fields:
        if not field.value or (
            isinstance(field.value, str) and field.value.strip() == ""
        ):
            missing_fields.append(field_name)
        elif field.confidence < min_confidence:
            low_confidence_fields.append(
                f"{field_name} (confidence: {field.confidence:.2f})"
            )

    if invoice.line_items:
        for i, item in enumerate(invoice.line_items):
            if item.confidence < min_confidence:
                low_confidence_fields.append(
                    f"line_item_{i} (confidence: {item.confidence:.2f})"
                )

    overall_confidence = calculate_overall_confidence_invoice(invoice)

    if missing_fields:
        validation_errors.append(
            f"Missing required fields: {', '.join(missing_fields)}"
        )
    if low_confidence_fields:
        validation_errors.append(
            f"Low confidence fields: {', '.join(low_confidence_fields)}"
        )

    is_valid = len(missing_fields) == 0 and overall_confidence >= min_confidence

    return ValidationResult(
        is_valid=is_valid,
        missing_fields=missing_fields,
        low_confidence_fields=low_confidence_fields,
        overall_confidence=overall_confidence,
        validation_errors=validation_errors,
    )


def validate_receipt_fields(
    receipt: ReceiptExtraction, min_confidence: float = 0.7
) -> ValidationResult:
    missing_fields = []
    low_confidence_fields = []
    validation_errors = []

    required_fields = [
        ("merchant_name", receipt.merchant_name),
        ("transaction_date", receipt.transaction_date),
        ("total_amount", receipt.total_amount),
    ]

    for field_name, field in required_fields:
        if not field.value or (
            isinstance(field.value, str) and field.value.strip() == ""
        ):
            missing_fields.append(field_name)
        elif field.confidence < min_confidence:
            low_confidence_fields.append(
                f"{field_name} (confidence: {field.confidence:.2f})"
            )

    if receipt.items:
        for i, item in enumerate(receipt.items):
            if item.confidence < min_confidence:
                low_confidence_fields.append(
                    f"item_{i} (confidence: {item.confidence:.2f})"
                )

    overall_confidence = calculate_overall_confidence_receipt(receipt)

    if missing_fields:
        validation_errors.append(
            f"Missing required fields: {', '.join(missing_fields)}"
        )
    if low_confidence_fields:
        validation_errors.append(
            f"Low confidence fields: {', '.join(low_confidence_fields)}"
        )

    is_valid = len(missing_fields) == 0 and overall_confidence >= min_confidence

    return ValidationResult(
        is_valid=is_valid,
        missing_fields=missing_fields,
        low_confidence_fields=low_confidence_fields,
        overall_confidence=overall_confidence,
        validation_errors=validation_errors,
    )


def validate_expense_record(expense: NormalizedExpense) -> ValidationResult:
    missing_fields = []
    validation_errors = []

    if not expense.expense_id or expense.expense_id.strip() == "":
        missing_fields.append("expense_id")
    if not expense.vendor or expense.vendor.strip() == "":
        missing_fields.append("vendor")
    if not expense.date:
        missing_fields.append("date")
    if expense.total_amount <= 0:
        validation_errors.append("Total amount must be greater than 0")
    if not expense.currency or expense.currency.strip() == "":
        missing_fields.append("currency")

    if expense.confidence_score < 0.5:
        validation_errors.append(
            f"Low overall confidence score: {expense.confidence_score:.2f}"
        )

    is_valid = len(missing_fields) == 0 and len(validation_errors) == 0

    return ValidationResult(
        is_valid=is_valid,
        missing_fields=missing_fields,
        low_confidence_fields=[],
        overall_confidence=expense.confidence_score,
        validation_errors=validation_errors,
    )


def calculate_overall_confidence_invoice(invoice: InvoiceExtraction) -> float:
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
        receipt.total_amount.confidence,
    ]
    if receipt.tax_amount.value:
        confidences.append(receipt.tax_amount.confidence)
    if receipt.items:
        item_confidences = [item.confidence for item in receipt.items]
        confidences.extend(item_confidences)

    return sum(confidences) / len(confidences) if confidences else 0.0


def get_validation_summary(validation: ValidationResult) -> Dict[str, Any]:
    return {
        "is_valid": validation.is_valid,
        "missing_fields_count": len(validation.missing_fields),
        "low_confidence_fields_count": len(validation.low_confidence_fields),
        "overall_confidence": validation.overall_confidence,
        "has_errors": len(validation.validation_errors) > 0,
    }
