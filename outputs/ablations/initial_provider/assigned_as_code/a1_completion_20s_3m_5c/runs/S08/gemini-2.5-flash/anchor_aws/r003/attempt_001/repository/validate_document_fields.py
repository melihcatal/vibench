import os
from document_models import NormalizedExpense
from google.cloud import logging # Provider-specific import

# Initialize Google Cloud Logging client
# Ensure GOOGLE_APPLICATION_CREDENTIALS environment variable is set
# or running in an environment with appropriate service account permissions.
logging_client = logging.Client()
logger = logging_client.logger("document_validation")

def validate_document_fields(expense: NormalizedExpense) -> bool:
    is_valid = True
    validation_messages = []

    if not expense.vendor_name:
        is_valid = False
        validation_messages.append("Vendor name is missing.")
    if not expense.transaction_date:
        is_valid = False
        validation_messages.append("Transaction date is missing.")
    if expense.total_amount is None:
        is_valid = False
        validation_messages.append("Total amount is missing.")
    elif not isinstance(expense.total_amount, (int, float)):
        is_valid = False
        validation_messages.append("Total amount is not a valid number.")
    
    # Example for confidence score (if it were available in NormalizedExpense or raw_extraction)
    # For now, assuming confidence_score might be set by the extraction step or a future step.
    if expense.confidence_score is not None and expense.confidence_score < 0.7:
        is_valid = False
        validation_messages.append(f"Low confidence score: {expense.confidence_score:.2f}")

    if not is_valid:
        expense.validation_status = "failed"
        log_message = f"Document validation failed for expense (Vendor: {expense.vendor_name}, Total: {expense.total_amount}): {\'; \'.join(validation_messages)}"
        logger.log_text(log_message, severity="ERROR")
    else:
        expense.validation_status = "success"
        log_message = f"Document validation successful for expense (Vendor: {expense.vendor_name}, Total: {expense.total_amount})"
        logger.log_text(log_message, severity="INFO")

    return is_valid
