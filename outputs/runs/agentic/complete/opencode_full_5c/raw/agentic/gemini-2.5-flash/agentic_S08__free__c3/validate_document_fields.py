from document_models import NormalizedExpense
from google.cloud import datastore
import os


def validate_document_fields(expense: NormalizedExpense) -> NormalizedExpense:
    client = datastore.Client(project=os.getenv("GOOGLE_CLOUD_PROJECT"))
    expense.validation_status = "VALIDATED"

    # Example: Fetch validation rules from Datastore
    query = client.query(kind="ValidationRule")
    query.add_filter("document_type", "=", expense.original_document_type)
    rules = list(query.fetch())

    required_fields = []
    for rule in rules:
        if rule.get("is_required", False):
            required_fields.append(rule.get("field_name"))

    # Basic validation logic
    if "vendor_name" in required_fields and not expense.vendor_name:
        expense.validation_status = "FAILED_VENDOR_MISSING"
    if "total_amount" in required_fields and (
        expense.total_amount is None or expense.total_amount <= 0
    ):
        expense.validation_status = "FAILED_TOTAL_INVALID"
    if "transaction_date" in required_fields and not expense.transaction_date:
        expense.validation_status = "FAILED_DATE_MISSING"

    # Add more complex validation rules as needed, e.g., date format, amount range, etc.

    return expense
