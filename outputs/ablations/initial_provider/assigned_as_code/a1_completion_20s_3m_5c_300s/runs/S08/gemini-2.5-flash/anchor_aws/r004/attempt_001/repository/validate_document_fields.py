import os
import json
from typing import Dict, Any, List
from document_models import NormalizedExpense, DocumentValidationResponse, ValidationResult
from document_client import get_aws_client

def validate_document_fields(document_id: str, expense: NormalizedExpense) -> DocumentValidationResponse:
    validation_results: List[ValidationResult] = []
    overall_valid = True

    # Example: Check for required fields
    required_fields = ["vendor_name", "transaction_date", "total_amount"]
    for field in required_fields:
        if getattr(expense, field) is None:
            validation_results.append(ValidationResult(field_name=field, is_valid=False, reason=f"{field} is missing"))
            overall_valid = False
        else:
            validation_results.append(ValidationResult(field_name=field, is_valid=True))

    # Example: Check confidence scores (if available)
    # Assuming confidence scores are part of the NormalizedExpense, e.g., expense.confidence_scores
    # For this example, we'll hardcode a dummy check.
    if expense.confidence_scores:
        for field, score in expense.confidence_scores.items():
            if score < 0.7: # Example threshold
                validation_results.append(ValidationResult(field_name=f"{field}_confidence", is_valid=False, reason=f"Confidence score {score} is below threshold"))
                overall_valid = False
            else:
                validation_results.append(ValidationResult(field_name=f"{field}_confidence", is_valid=True))

    # Integrate with an external validation service (e.g., AWS Lambda)
    # This demonstrates a concrete provider interaction even if the Lambda's logic isn't defined here.
    lambda_client = get_aws_client("lambda", region_name=os.environ.get("AWS_REGION"))
    lambda_function_name = os.environ.get("VALIDATION_LAMBDA_FUNCTION_NAME", "document-validation-service")
    
    try:
        payload = {"document_id": document_id, "expense_data": expense.dict()}
        response = lambda_client.invoke(
            FunctionName=lambda_function_name,
            InvocationType='RequestResponse',  # Or 'Event' for async invocation
            Payload=json.dumps(payload)
        )
        
        # Parse the response from the Lambda if needed
        lambda_response_payload = json.loads(response['Payload'].read().decode('utf-8'))
        # Example: if lambda_response_payload has an 'external_checks_valid' field
        if not lambda_response_payload.get("external_checks_valid", True):
            overall_valid = False
            validation_results.append(ValidationResult(field_name="external_validation", is_valid=False, reason="External validation service reported issues"))

    except Exception as e:
        print(f"Error invoking external validation service: {e}")
        validation_results.append(ValidationResult(field_name="external_validation_service", is_valid=False, reason=f"Failed to invoke external service: {str(e)}"))
        overall_valid = False

    return DocumentValidationResponse(
        document_id=document_id,
        overall_valid=overall_valid,
        validation_results=validation_results
    )
