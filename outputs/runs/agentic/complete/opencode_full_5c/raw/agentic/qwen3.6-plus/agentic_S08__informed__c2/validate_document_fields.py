from typing import List, Optional, Dict, Any, Union

from document_models import (
    InvoiceExtractionResult,
    ReceiptExtractionResult,
    NormalizedExpenseRecord,
    validate_invoice_fields,
    validate_receipt_fields,
    validate_expense_record,
    REQUIRED_INVOICE_FIELDS,
    REQUIRED_RECEIPT_FIELDS,
    MINIMUM_CONFIDENCE_THRESHOLD,
)


def validate_document_fields(
    extraction_result: Union[InvoiceExtractionResult, ReceiptExtractionResult],
    required_fields: Optional[List[str]] = None,
    min_confidence: float = MINIMUM_CONFIDENCE_THRESHOLD,
) -> Dict[str, Any]:
    if isinstance(extraction_result, InvoiceExtractionResult):
        fields_to_check = required_fields or REQUIRED_INVOICE_FIELDS
        result = validate_invoice_fields(
            extraction_result, required_fields=fields_to_check
        )
    elif isinstance(extraction_result, ReceiptExtractionResult):
        fields_to_check = required_fields or REQUIRED_RECEIPT_FIELDS
        result = validate_receipt_fields(
            extraction_result, required_fields=fields_to_check
        )
    else:
        raise ValueError(
            f"Unsupported extraction result type: {type(extraction_result)}"
        )

    if min_confidence != MINIMUM_CONFIDENCE_THRESHOLD:
        low_conf = []
        for entry in result.get("low_confidence_fields", []):
            if entry["confidence"] < min_confidence:
                low_conf.append(entry)
        result["low_confidence_fields"] = low_conf
        result["valid"] = len(result["missing_fields"]) == 0 and len(low_conf) == 0

    return result


def validate_normalized_expense(
    record: NormalizedExpenseRecord,
) -> Dict[str, Any]:
    return validate_expense_record(record)


def validate_batch_documents(
    extraction_results: list,
    required_fields: Optional[List[str]] = None,
    min_confidence: float = MINIMUM_CONFIDENCE_THRESHOLD,
) -> List[Dict[str, Any]]:
    validations = []
    for result in extraction_results:
        validations.append(
            validate_document_fields(
                result, required_fields=required_fields, min_confidence=min_confidence
            )
        )
    return validations
