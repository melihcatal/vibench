import json
from typing import List, Dict, Any
from document_models import NormalizedExpense, ValidationResult
from document_client import get_gemini_client


def validate_document_fields(
    expense_record: NormalizedExpense,
    required_fields: List[str],
    confidence_threshold: float = 0.7,
) -> ValidationResult:
    """
    Validates required structured fields and confidence scores using Google Gemini API
    for nuanced validation and to provide actionable feedback.
    """
    client = get_gemini_client()

    missing_fields = []
    low_confidence_fields = {}

    # Basic structural validation
    for field in required_fields:
        if not getattr(expense_record, field, None):
            missing_fields.append(field)

    # Confidence score validation
    for field, score in expense_record.confidence_scores.items():
        if score < confidence_threshold:
            low_confidence_fields[field] = score

    is_valid_structural = not missing_fields
    is_valid_confidence = not low_confidence_fields

    if is_valid_structural and is_valid_confidence:
        return ValidationResult(
            is_valid=True,
            message="Document fields are valid and meet confidence thresholds.",
        )

    # If not valid, use Gemini for a more intelligent message
    prompt_parts = [
        f"You are an AI assistant that provides validation feedback for extracted document fields. "
        f"Given the normalized expense record, a list of required fields, and fields with low confidence, "
        f"generate a concise and helpful validation message. "
        f"The required fields are: {', '.join(required_fields)}. "
        f"The confidence threshold is {confidence_threshold}.\n\n",
        f"Normalized Expense Record:\n{json.dumps(expense_record.__dict__, indent=2)}\n\n",
        f"Missing Fields: {missing_fields if missing_fields else 'None'}\n",
        f"Low Confidence Fields: {low_confidence_fields if low_confidence_fields else 'None'}\n\n",
        "Generate a detailed validation message explaining what needs to be corrected. Start with 'Validation Failed:'",
    ]

    response = client.generate_content(prompt_parts)

    return ValidationResult(
        is_valid=False,
        missing_fields=missing_fields,
        low_confidence_fields=low_confidence_fields,
        message=response.text.strip(),
    )
