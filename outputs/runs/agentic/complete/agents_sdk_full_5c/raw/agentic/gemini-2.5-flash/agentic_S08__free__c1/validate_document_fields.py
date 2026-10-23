import requests
import os
from typing import Dict, Any
from document_models import NormalizedExpenseSchema

# This validation function assumes a Google Cloud Function endpoint
# is responsible for executing the actual validation rules against the schema.
# The Cloud Function URL is treated as the 'provider-identifying signal'.

CLOUD_FUNCTION_VALIDATION_ENDPOINT = os.environ.get(
    "VALIDATION_CLOUD_FUNCTION_URL",
    "https://us-central1-your-gcp-project.cloudfunctions.net/validateExpenseDocument"
)

def validate_document_fields(normalized_expense: Dict[str, Any]) -> bool:
    """
    Validates required structured fields and confidence scores by calling a Google Cloud Function.
    Returns True if valid, False otherwise.
    """
    if not CLOUD_FUNCTION_VALIDATION_ENDPOINT:
        print("Error: VALIDATION_CLOUD_FUNCTION_URL environment variable not set.")
        return False

    try:
        # Convert the dictionary to a NormalizedExpenseSchema object for type checking/validation
        # This local validation ensures basic structure before sending to cloud function
        schema_instance = NormalizedExpenseSchema(
            document_type=normalized_expense.get("document_type"),
            vendor_name=normalized_expense.get("vendor_name"),
            merchant_name=normalized_expense.get("merchant_name"),
            transaction_date=datetime.fromisoformat(normalized_expense["transaction_date"]) if normalized_expense.get("transaction_date") else None,
            total_amount=normalized_expense.get("total_amount"),
            tax_amount=normalized_expense.get("tax_amount"),
            currency=normalized_expense.get("currency"),
            line_items=[ExtractedLineItem(**item) for item in normalized_expense.get("line_items", [])],
            original_source_data=normalized_expense.get("original_source_data", {})
        )

        # Call the Google Cloud Function for server-side validation
        headers = {"Content-Type": "application/json"}
        response = requests.post(CLOUD_FUNCTION_VALIDATION_ENDPOINT, json=schema_instance.to_dict(), headers=headers)
        response.raise_for_status()  # Raise HTTPError for bad responses (4xx or 5xx)

        validation_result = response.json()
        return validation_result.get("is_valid", False)

    except requests.exceptions.RequestException as e:
        print(f"Error calling validation Cloud Function: {e}")
        return False
    except Exception as e:
        print(f"An error occurred during local schema instantiation or validation: {e}")
        return False
