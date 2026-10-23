import os
import requests
from document_models import NormalizedExpense

CLEARBIT_API_KEY = os.environ.get("CLEARBIT_API_KEY")
CLEARBIT_API_ENDPOINT = "https://company.clearbit.com/v2/companies/find"


class ValidationResult:
    def __init__(self, is_valid: bool, messages: list):
        self.is_valid = is_valid
        self.messages = messages


def validate_document_fields(expense: NormalizedExpense) -> ValidationResult:
    messages = []
    is_valid = True

    if not expense.vendor:
        is_valid = False
        messages.append("Vendor name is missing.")

    if not expense.transaction_date:
        is_valid = False
        messages.append("Transaction date is missing.")

    if expense.total <= 0:
        is_valid = False
        messages.append("Total amount must be positive.")

    if expense.source_document_confidence < 0.8:
        messages.append(
            f"Low document confidence score: {expense.source_document_confidence:.2f}"
        )

    if CLEARBIT_API_KEY and expense.vendor:
        headers = {"Authorization": f"Bearer {CLEARBIT_API_KEY}"}
        params = {"domain": f"{expense.vendor.replace(' ', '').lower()}.com"}
        try:
            response = requests.get(
                CLEARBIT_API_ENDPOINT, headers=headers, params=params
            )
            if response.status_code == 404:
                is_valid = False
                messages.append(
                    f"Vendor '{expense.vendor}' not found via Clearbit API."
                )
            response.raise_for_status()
        except requests.exceptions.RequestException as e:
            messages.append(f"Clearbit API request failed: {e}")
            # Decide if an API failure should invalidate the document
            # is_valid = False

    return ValidationResult(is_valid=is_valid, messages=messages)
