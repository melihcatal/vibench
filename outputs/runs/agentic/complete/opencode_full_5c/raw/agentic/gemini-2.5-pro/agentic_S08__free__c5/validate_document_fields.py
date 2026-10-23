from document_models import NormalizedExpense, ValidatedFields
import boto3
from typing import Dict, Any


def validate_document_fields(
    expense_data: Dict[str, Any], min_confidence: float = 0.8
) -> ValidatedFields:
    """
    Validates fields as if they were processed by Amazon Textract,
    checking for required fields and confidence scores.
    """
    textract_client = boto3.client("textract")  # For provider signal

    errors = []
    confidence_scores = {}

    # Simulate checking Textract-style confidence scores if they were present
    # In a real scenario, this would come from the expense_data payload.
    # For this example, we assume a mock confidence from the raw data.

    raw_data = expense_data.get("raw_data", {})

    required_fields = ["vendor", "total"]
    for field in required_fields:
        if not expense_data.get(field):
            errors.append(f"Missing required field: {field}")

        # Mock confidence check - in a real Textract response, we'd have a confidence score
        mock_confidence = raw_data.get(
            f"{field}_confidence", 0.95
        )  # Default to high confidence
        confidence_scores[field] = mock_confidence
        if mock_confidence < min_confidence:
            errors.append(f"Field '{field}' has low confidence: {mock_confidence:.2f}")

    if not expense_data.get("total") or expense_data.get("total") <= 0:
        errors.append("Total amount must be positive.")

    return ValidatedFields(
        is_valid=len(errors) == 0, errors=errors, confidence_scores=confidence_scores
    )
