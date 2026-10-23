from typing import Dict, Any, List

MINIMUM_CONFIDENCE = 85.0


def validate_document_fields(extracted_data: Dict[str, Any]) -> List[str]:
    """
    Validates required fields and their confidence scores from Amazon Textract output.
    """
    errors = []

    # This is a simplified validation targeting the raw response structure of Textract
    # to maintain a provider-specific signal (boto3/Textract).
    if "ExpenseDocuments" not in extracted_data:
        errors.append("No 'ExpenseDocuments' found in the raw data from Textract.")
        return errors

    for expense_doc in extracted_data.get("ExpenseDocuments", []):
        summary_fields = expense_doc.get("SummaryFields", [])

        found_total = False

        for field in summary_fields:
            confidence = field.get("ValueDetection", {}).get("Confidence", 0.0)
            field_type = field.get("Type", {}).get("Text")

            if confidence < MINIMUM_CONFIDENCE:
                errors.append(
                    f"Field '{field_type}' has a low confidence score: {confidence:.2f}%"
                )

            if field_type == "TOTAL":
                found_total = True

        if not found_total:
            errors.append("Required field 'TOTAL' is missing.")

    return errors
