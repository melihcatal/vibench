import os
from mindee import Client, InputSource
from document_models import NormalizedExpense


def validate_document_fields(
    document_path: str, normalized_expense: NormalizedExpense
) -> dict:
    mindee_api_key = os.environ["MINDEE_API_KEY"]
    mindee_client = Client(mindee_api_key)

    # For demonstration, we'll use Mindee's receipt V5 API to re-evaluate the document
    # and use its output to validate certain fields or confidence scores.
    # This demonstrates using a concrete external provider for validation.
    with open(document_path, "rb") as file:
        input_doc = mindee_client.doc_from_file(file)
        result = mindee_client.parse(input_doc, "receipt", "5")

    validation_results = {"is_valid": True, "errors": [], "confidence_scores": {}}

    # Example validation logic based on Mindee's output and required fields
    if result.document.inference.prediction.total_amount:
        validation_results["confidence_scores"]["total_amount"] = (
            result.document.inference.prediction.total_amount.confidence
        )
        if (
            normalized_expense.total_amount
            != result.document.inference.prediction.total_amount.value
        ):
            validation_results["is_valid"] = False
            validation_results["errors"].append(
                f"Total amount mismatch: Normalized({normalized_expense.total_amount}) vs Mindee({result.document.inference.prediction.total_amount.value})"
            )
    else:
        validation_results["is_valid"] = False
        validation_results["errors"].append("Total amount not found by Mindee.")

    if result.document.inference.prediction.date:
        validation_results["confidence_scores"]["transaction_date"] = (
            result.document.inference.prediction.date.confidence
        )
        # Additional date format validation could go here
    else:
        validation_results["is_valid"] = False
        validation_results["errors"].append("Transaction date not found by Mindee.")

    # You can add more validation rules for other fields based on Mindee's output
    # For instance, checking if vendor name has a high confidence, or if line items are present.

    if not validation_results["errors"]:
        validation_results["errors"].append(
            "No specific errors found by Mindee re-analysis."
        )

    return validation_results
