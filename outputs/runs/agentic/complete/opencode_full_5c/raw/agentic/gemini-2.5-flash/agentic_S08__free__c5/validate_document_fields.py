from typing import List, Dict, Any
from document_models import (
    InvoiceExtractionResult,
    ReceiptExtractionResult,
    NormalizedExpense,
    ValidationResult,
    DocumentField,
)
from document_client import get_logging_client
import logging

# Configure a logger for this module
logger = get_logging_client().logger("document_validation")


def validate_document_fields(
    extracted_data: Union[InvoiceExtractionResult, ReceiptExtractionResult],
    min_confidence: float = 0.7,
    required_fields: List[str] = None,
) -> List[ValidationResult]:
    validation_results: List[ValidationResult] = []

    if required_fields is None:
        # Define default required fields based on document type if not provided
        if isinstance(extracted_data, InvoiceExtractionResult):
            required_fields = [
                "vendor_name",
                "invoice_date",
                "total_amount",
                "currency",
            ]
        elif isinstance(extracted_data, ReceiptExtractionResult):
            required_fields = [
                "merchant_name",
                "transaction_date",
                "total_amount",
                "currency",
            ]
        else:
            return [
                ValidationResult(
                    field_name="document_type",
                    is_valid=False,
                    reason="Unknown document type.",
                )
            ]

    # Validate required fields and confidence
    for field_name in required_fields:
        doc_field: Optional[DocumentField] = getattr(extracted_data, field_name, None)

        if not doc_field or not doc_field.value:
            validation_results.append(
                ValidationResult(
                    field_name=field_name,
                    is_valid=False,
                    reason=f"Required field '{field_name}' is missing or empty.",
                    extracted_value=doc_field.value if doc_field else None,
                    actual_confidence=doc_field.confidence if doc_field else 0.0,
                )
            )
            logger.log_text(
                f"Validation FAILED: Required field '{field_name}' is missing or empty. Document type: {type(extracted_data).__name__}",
                severity="WARNING",
            )
        elif doc_field.confidence < min_confidence:
            validation_results.append(
                ValidationResult(
                    field_name=field_name,
                    is_valid=False,
                    reason=f"Confidence for '{field_name}' ({doc_field.confidence:.2f}) is below required minimum ({min_confidence:.2f}).",
                    extracted_value=doc_field.value,
                    expected_confidence=min_confidence,
                    actual_confidence=doc_field.confidence,
                )
            )
            logger.log_text(
                f"Validation FAILED: Confidence for '{field_name}' below threshold. Value: {doc_field.value}, Confidence: {doc_field.confidence:.2f}. Document type: {type(extracted_data).__name__}",
                severity="WARNING",
            )
        else:
            validation_results.append(
                ValidationResult(
                    field_name=field_name,
                    is_valid=True,
                    reason="Field is present and confidence is sufficient.",
                    extracted_value=doc_field.value,
                    expected_confidence=min_confidence,
                    actual_confidence=doc_field.confidence,
                )
            )
            logger.log_text(
                f"Validation PASSED: Field '{field_name}'. Value: {doc_field.value}, Confidence: {doc_field.confidence:.2f}. Document type: {type(extracted_data).__name__}",
                severity="INFO",
            )

    # Validate line items if present (optional, can be extended)
    if (
        isinstance(extracted_data, (InvoiceExtractionResult, ReceiptExtractionResult))
        and extracted_data.line_items
    ):
        for i, item in enumerate(extracted_data.line_items):
            if item.confidence < min_confidence:
                validation_results.append(
                    ValidationResult(
                        field_name=f"line_item[{i}]",
                        is_valid=False,
                        reason=f"Confidence for line item {i} ({item.confidence:.2f}) is below required minimum ({min_confidence:.2f}).",
                        extracted_value=item.description,
                        expected_confidence=min_confidence,
                        actual_confidence=item.confidence,
                    )
                )
                logger.log_text(
                    f"Validation FAILED: Confidence for line item {i} below threshold. Description: {item.description}, Confidence: {item.confidence:.2f}. Document type: {type(extracted_data).__name__}",
                    severity="WARNING",
                )

    return validation_results
