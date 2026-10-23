import os
from google.cloud import logging
from document_models import NormalizedExpense
from typing import Dict, Any

PROJECT_ID = os.environ.get("GCP_PROJECT_ID")
LOG_NAME = "document-validation-logs"


def get_logger_client():
    if not PROJECT_ID:
        raise ValueError("GCP_PROJECT_ID must be set as an environment variable.")
    return logging.Client(project=PROJECT_ID)


def validate_document_fields(
    expense_record: NormalizedExpense, min_confidence: float = 0.7
) -> Dict[str, Any]:
    validation_results = {
        "is_valid": True,
        "missing_fields": [],
        "low_confidence_fields": [],
        "warnings": [],
    }

    required_fields = [
        "vendor_merchant_name",
        "transaction_date",
        "total_amount",
        "currency",
    ]

    for field in required_fields:
        if getattr(expense_record, field) is None:
            validation_results["is_valid"] = False
            validation_results["missing_fields"].append(field)

    if expense_record.total_amount is not None and expense_record.total_amount < 0:
        validation_results["is_valid"] = False
        validation_results["warnings"].append("Total amount is negative.")

    if not expense_record.line_items and expense_record.document_type == "invoice":
        validation_results["warnings"].append("Invoice has no line items.")

    # Log the validation results to Google Cloud Logging
    logger = get_logger_client().logger(LOG_NAME)
    log_entry = {
        "document_type": expense_record.document_type,
        "record_id": expense_record.original_document_data.get(
            "id", "N/A"
        ),  # Assuming an ID might be present
        "validation_results": validation_results,
    }
    logger.log_struct(
        log_entry, severity="INFO" if validation_results["is_valid"] else "ERROR"
    )

    return validation_results
