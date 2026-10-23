import os
import json
import requests
from google.auth.transport.requests import Request
from google.oauth2 import id_token
from typing import Dict, Any

from document_models import NormalizedExpense, DocumentValidationResult, FieldValidation

def validate_document_fields(normalized_expense: NormalizedExpense) -> DocumentValidationResult:
    # Google Cloud Function endpoint for validation
    cloud_function_url = os.environ.get("VALIDATION_CLOUD_FUNCTION_URL")
    if not cloud_function_url:
        raise ValueError("VALIDATION_CLOUD_FUNCTION_URL environment variable not set.")

    # The target audience for the ID token. For Cloud Functions, this is typically the function's URL.
    target_audience = cloud_function_url

    # Get the ID token for authentication
    auth_req = Request()
    try:
        id_token_jwt = id_token.fetch_id_token(auth_req, target_audience)
    except Exception as e:
        raise RuntimeError(f"Could not fetch ID token for Cloud Function: {e}")

    headers = {
        "Authorization": f"Bearer {id_token_jwt}",
        "Content-Type": "application/json"
    }

    # Prepare the payload for the Cloud Function
    # The Cloud Function would contain the actual validation logic against a set of rules and confidence thresholds
    payload = {
        "document_id": f"expense-{normalized_expense.vendor_name}-{normalized_expense.transaction_date}",
        "normalized_expense": normalized_expense.dict() # Convert Pydantic model to dict
    }

    try:
        response = requests.post(cloud_function_url, headers=headers, json=payload)
        response.raise_for_status() # Raise an HTTPError for bad responses (4xx or 5xx)
        
        validation_result_data = response.json()
        
        # Convert dictionaries back to Pydantic models
        validation_details = [
            FieldValidation(**detail) for detail in validation_result_data.get("validation_details", [])
        ]
        
        return DocumentValidationResult(
            document_id=validation_result_data.get("document_id", ""),
            is_document_valid=validation_result_data.get("is_document_valid", False),
            validation_details=validation_details
        )

    except requests.exceptions.RequestException as e:
        print(f"Error communicating with Google Cloud Function: {e}")
        if e.response:
            print(f"Cloud Function response: {e.response.text}")
        raise
    except json.JSONDecodeError as e:
        print(f"Error decoding JSON from Cloud Function response: {e}")
        print(f"Raw response content: {response.text}")
        raise
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        raise
