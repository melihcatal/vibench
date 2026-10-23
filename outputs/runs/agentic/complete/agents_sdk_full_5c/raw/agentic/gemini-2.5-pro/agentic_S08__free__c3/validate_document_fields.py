import os
import requests
from typing import Dict, Any, List, Tuple


def validate_document_fields(
    extracted_data: Dict[str, Any]
) -> Tuple[bool, List[str]]:
    """
    Validates required fields and confidence scores.
    Uses AbstractAPI for a sample external email validation check.
    """
    errors = []
    is_valid = True

    # Basic presence checks
    required_fields = ["vendor_name", "total_amount", "invoice_date"]
    for field in required_fields:
        if not extracted_data.get(field):
            errors.append(f"Missing required field: {field}")
            is_valid = False

    # Value checks
    total = extracted_data.get("total_amount", 0)
    if not isinstance(total, (int, float)) or total <= 0:
        errors.append(f"Invalid total_amount: {total}")
        is_valid = False

    # External API validation example for a hypothetical vendor email field
    vendor_email = extracted_data.get("vendor_email")
    if vendor_email:
        api_key = os.environ.get("ABSTRACT_API_KEY")
        if not api_key:
            errors.append("ABSTRACT_API_KEY not set for email validation.")
        else:
            try:
                response = requests.get(
                    "https://emailvalidation.abstractapi.com/v1/",
                    params={"api_key": api_key, "email": vendor_email}
                )
                response.raise_for_status()
                validation_result = response.json()
                if validation_result.get("is_valid_format", {}).get("value") is not True:
                     errors.append(f"Invalid vendor email format: {vendor_email}")
                     is_valid = False
            except requests.exceptions.RequestException as e:
                errors.append(f"Email validation API call failed: {e}")

    return is_valid, errors
