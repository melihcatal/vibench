import os
from typing import Tuple
import cohere
from document_client import get_cohere_client
from document_models import NormalizedExpense, DocumentValidationResult

def validate_document_fields(expense_record: NormalizedExpense) -> DocumentValidationResult:
    client = get_cohere_client()

    # Define validation rules (can be extended)
    min_total_amount = 0.01
    required_fields = [
        "transaction_type",
        "vendor_name",
        "transaction_date",
        "total_amount",
        "currency",
        "line_items"
    ]

    validation_errors = []

    # Basic structural validation
    for field in required_fields:
        if not getattr(expense_record, field):
            validation_errors.append(f"Missing required field: {field}")

    if expense_record.total_amount <= min_total_amount:
        validation_errors.append(f"Total amount must be greater than {min_total_amount}")

    if not expense_record.currency or len(expense_record.currency) != 3:
        validation_errors.append("Currency must be a 3-letter code (e.g., USD).")

    # Semantic validation using Cohere
    if not validation_errors:
        chat_response = client.chat(
            model="command-r", # or command-r-plus for better quality
            message=f"Review the following expense record for completeness, consistency, and general reasonableness. If there are any potential issues or red flags, identify them. Otherwise, state that it looks good.\n\n{expense_record.model_dump_json(indent=2)}",
            preamble="You are an AI assistant tasked with identifying potential anomalies or missing information in expense reports. Focus on semantic correctness and data quality beyond simple structural checks."
        )

        ai_validation_feedback = chat_response.text
        is_valid = "looks good" in ai_validation_feedback.lower() and not validation_errors

        if not is_valid:
            validation_errors.append(f"AI feedback: {ai_validation_feedback}")

    is_valid_overall = len(validation_errors) == 0

    return DocumentValidationResult(
        is_valid=is_valid_overall,
        validation_errors=validation_errors if not is_valid_overall else []
    )
