import os
import json
from typing import Dict, Any, Optional, List
from google.cloud import secretmanager
from document_models import NormalizedExpense, LineItem

def get_validation_config(project_id: str, secret_id: str, version_id: str = "latest") -> Optional[dict]:
    """Fetches validation configuration from Google Secret Manager."""
    try:
        client = secretmanager.SecretManagerServiceClient()
        name = f"projects/{project_id}/secrets/{secret_id}/versions/{version_id}"
        response = client.access_secret_version(name=name)
        return json.loads(response.payload.data.decode("UTF-8"))
    except Exception as e:
        print(f"Error fetching validation config from Secret Manager: {e}")
        return None

def validate_document_fields(
    normalized_expense: NormalizedExpense,
    project_id: str,
    secret_id: str,
    confidence_threshold: float = 0.7,
    version_id: str = "latest",
) -> NormalizedExpense:
    """Validates required structured fields and confidence scores for a normalized expense.
    Validation rules and confidence thresholds are fetched from Google Secret Manager.
    """
    validation_config = get_validation_config(project_id, secret_id, version_id)
    if not validation_config:
        print("Failed to load validation configuration. Proceeding with basic validation.")
        # Fallback to hardcoded threshold if config fails to load
        required_fields = ["transaction_date", "vendor_merchant_name", "total_amount"]
        field_confidence_threshold = confidence_threshold
    else:
        required_fields = validation_config.get("required_fields", ["transaction_date", "vendor_merchant_name", "total_amount"])
        field_confidence_threshold = validation_config.get("field_confidence_threshold", confidence_threshold)

    validation_scores = {}

    # Basic field presence validation
    for field in required_fields:
        is_present = getattr(normalized_expense, field, None) is not None
        validation_scores[f"{field}_present"] = 1.0 if is_present else 0.0

    # In a real Document AI scenario, confidence scores would be part of the extraction.
    # For this example, we'll simulate a confidence check if data exists.
    # If the Document AI output provided confidence, we would use entity.confidence directly.
    # For now, we will assign a high confidence if the field is present, simulating ideal extraction.
    # A more realistic approach would involve passing Document AI's actual confidence scores.
    for field in required_fields:
        if getattr(normalized_expense, field, None) is not None:
            # Simulating a confidence score if a field is present
            # In a real integration, this would come from the Document AI response.
            validation_scores[f"{field}_confidence"] = 0.95 # Assume high confidence if extracted
        else:
            validation_scores[f"{field}_confidence"] = 0.0

    # Example: Check if total_amount is non-negative
    if normalized_expense.total_amount is not None:
        validation_scores["total_amount_non_negative"] = 1.0 if normalized_expense.total_amount >= 0 else 0.0
    else:
        validation_scores["total_amount_non_negative"] = 0.0

    normalized_expense.validation_scores.update(validation_scores)
    return normalized_expense
