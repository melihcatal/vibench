from typing import Union, List, Dict, Any
from document_models import (
    ExtractedInvoiceFields,
    ExtractedReceiptFields,
    ValidationReport,
)

REQUIRED_INVOICE_FIELDS = ["vendor_name", "invoice_id", "invoice_date", "total"]

REQUIRED_RECEIPT_FIELDS = ["merchant_name", "transaction_date", "total"]

CONFIDENCE_THRESHOLD = 0.7


def validate_document_fields(
    extracted_data: Union[ExtractedInvoiceFields, ExtractedReceiptFields],
    document_type: str,
    confidence_threshold: float = CONFIDENCE_THRESHOLD,
) -> ValidationReport:
    missing_fields = []
    low_confidence_fields = []

    if document_type == "invoice":
        required_fields = REQUIRED_INVOICE_FIELDS
        confidence_scores = extracted_data.confidence_scores
        field_values = {
            "vendor_name": extracted_data.vendor_name,
            "invoice_id": extracted_data.invoice_id,
            "invoice_date": extracted_data.invoice_date,
            "total": extracted_data.total,
        }
    elif document_type == "receipt":
        required_fields = REQUIRED_RECEIPT_FIELDS
        confidence_scores = extracted_data.confidence_scores
        field_values = {
            "merchant_name": extracted_data.merchant_name,
            "transaction_date": extracted_data.transaction_date,
            "total": extracted_data.total,
        }
    else:
        return ValidationReport(
            is_valid=False,
            missing_fields=["unknown_document_type"],
            low_confidence_fields=[],
            confidence_threshold=confidence_threshold,
            details={"error": f"Unsupported document type: {document_type}"},
        )

    for field_name in required_fields:
        value = field_values.get(field_name)
        if value is None or value == "" or value == 0.0:
            missing_fields.append(field_name)

    for field_name, score in confidence_scores.items():
        if score < confidence_threshold:
            low_confidence_fields.append(field_name)

    is_valid = len(missing_fields) == 0 and len(low_confidence_fields) == 0

    return ValidationReport(
        is_valid=is_valid,
        missing_fields=missing_fields,
        low_confidence_fields=low_confidence_fields,
        confidence_threshold=confidence_threshold,
        details={
            "document_type": document_type,
            "total_fields_checked": len(required_fields),
            "fields_passed": len(required_fields) - len(missing_fields),
        },
    )


def validate_batch_documents(
    documents: List[Dict[str, Any]], confidence_threshold: float = CONFIDENCE_THRESHOLD
) -> List[ValidationReport]:
    reports = []
    for doc in documents:
        extracted_data = doc["extracted_data"]
        document_type = doc["document_type"]
        report = validate_document_fields(
            extracted_data, document_type, confidence_threshold
        )
        reports.append(report)
    return reports


def get_validation_summary(reports: List[ValidationReport]) -> Dict[str, Any]:
    total = len(reports)
    valid_count = sum(1 for r in reports if r.is_valid)
    invalid_count = total - valid_count
    all_missing = []
    all_low_confidence = []
    for r in reports:
        all_missing.extend(r.missing_fields)
        all_low_confidence.extend(r.low_confidence_fields)

    return {
        "total_documents": total,
        "valid_documents": valid_count,
        "invalid_documents": invalid_count,
        "validation_rate": valid_count / total if total > 0 else 0.0,
        "common_missing_fields": list(set(all_missing)),
        "common_low_confidence_fields": list(set(all_low_confidence)),
    }
