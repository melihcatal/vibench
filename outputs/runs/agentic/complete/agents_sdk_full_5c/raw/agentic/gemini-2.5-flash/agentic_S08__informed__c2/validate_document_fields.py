import os
from google.cloud import logging
from document_models import NormalizedExpense

# Initialize Google Cloud Logging client
# GOOGLE_APPLICATION_CREDENTIALS should be set or default credentials configured
logging_client = logging.Client()
logger = logging_client.logger("document_validation_logger")

def validate_document_fields(expense: NormalizedExpense, required_fields: list[str]) -> bool:
    is_valid = True
    missing_fields = []

    for field in required_fields:
        # Check if the field exists and is not empty/None
        field_value = getattr(expense, field, None)
        if field_value is None or (isinstance(field_value, str) and not field_value.strip()):
            missing_fields.append(field)
            is_valid = False

    if not is_valid:
        log_message = f"Validation failed for expense from vendor '{expense.vendor}'. Missing fields: {', '.join(missing_fields)}"
        logger.log_text(log_message, severity="ERROR")
        print(f"ERROR: {log_message}")
    else:
        log_message = f"Validation successful for expense from vendor '{expense.vendor}'."
        logger.log_text(log_message, severity="INFO")
        print(f"INFO: {log_message}")

    return is_valid

if __name__ == '__main__':
    # Example usage:
    # from document_models import NormalizedExpense, LineItem
    # expense_data = NormalizedExpense(
    #     vendor="Example Vendor",
    #     date="2023-10-26",
    #     amount=150.75,
    #     currency="USD",
    #     description="Office Supplies",
    #     line_items=[LineItem(description="Pens", amount=10.0), LineItem(description="Paper", amount=140.75)]
    # )
    #
    # required_fields = ["vendor", "amount", "currency"]
    # is_valid = validate_document_fields(expense_data, required_fields)
    # print(f"Document valid: {is_valid}")
    #
    # invalid_expense_data = NormalizedExpense(
    #     vendor="", # Missing vendor
    #     date="2023-10-26",
    #     amount=150.75,
    #     currency="USD",
    #     description="Office Supplies",
    #     line_items=[]
    # )
    # is_valid_invalid = validate_document_fields(invalid_expense_data, required_fields)
    # print(f"Document valid (invalid case): {is_valid_invalid}")
    pass
