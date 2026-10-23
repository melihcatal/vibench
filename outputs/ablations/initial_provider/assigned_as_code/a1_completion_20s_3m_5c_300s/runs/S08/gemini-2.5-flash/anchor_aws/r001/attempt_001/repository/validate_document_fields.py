import boto3
from typing import Dict, Any, List
from document_models import NormalizedExpense
from document_client import load_config, get_aws_client

def validate_document_fields(normalized_expense_data: Dict[str, Any]) -> Dict[str, Any]:
    config = load_config()
    region = config.get("aws_region")
    comprehend_language_code = config.get("aws_comprehend_language_code")

    if not all([region, comprehend_language_code]):
        raise ValueError("AWS region or Comprehend language code is not configured.")

    client = get_aws_client("comprehend", region)

    normalized_expense = NormalizedExpense(**normalized_expense_data["normalized_expense"])

    validation_results = {"is_valid": True, "errors": []}

    # Example validation: Check if vendor name is present
    if not normalized_expense.vendor_name:
        validation_results["is_valid"] = False
        validation_results["errors"].append({"field": "vendor_name", "message": "Vendor name is missing."})

    # Example validation using AWS Comprehend for transaction date
    if normalized_expense.transaction_date:
        try:
            response = client.detect_entities(
                Text=normalized_expense.transaction_date,
                LanguageCode=comprehend_language_code
            )
            date_entities = [entity for entity in response["Entities"] if entity["Type"] == "DATE"]
            if not date_entities:
                validation_results["is_valid"] = False
                validation_results["errors"].append({"field": "transaction_date", "message": "Transaction date is not recognized as a valid date."})
        except Exception as e:
            validation_results["is_valid"] = False
            validation_results["errors"].append({"field": "transaction_date", "message": f"Comprehend entity detection failed: {str(e)}"})        
    else:
        validation_results["is_valid"] = False
        validation_results["errors"].append({"field": "transaction_date", "message": "Transaction date is missing."})

    # Add more validation logic as needed

    return {"validation_results": validation_results}
