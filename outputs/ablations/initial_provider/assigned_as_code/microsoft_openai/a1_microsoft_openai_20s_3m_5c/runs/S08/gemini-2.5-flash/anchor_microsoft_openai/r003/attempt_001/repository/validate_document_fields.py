import os
from typing import Dict, Any, List
from google.cloud import aiplatform
from google.protobuf import json_format
from google.cloud.aiplatform.gapic.schema import predict_pb2


def validate_document_fields(normalized_expense: Dict[str, Any], config: Dict[str, Any] = None) -> Dict[str, Any]:
    config = config or {}
    project_id = os.environ.get("GOOGLE_CLOUD_PROJECT_ID", config.get("project_id"))
    location = os.environ.get("GOOGLE_CLOUD_LOCATION", config.get("location", "us-central1"))
    publisher = "google"
    model_id = "gemini-1.0-pro"

    if not all([project_id, location]):
        raise ValueError("Missing GOOGLE_CLOUD_PROJECT_ID or GOOGLE_CLOUD_LOCATION environment variables or config values.")

    aiplatform.init(project=project_id, location=location)

    # Prepare the prompt for the Gemini model to validate the expense data
    prompt = f"""Review the following expense record and identify any potential validation errors or inconsistencies.\n\nExpense Record:\n{normalized_expense}\n\nValidation criteria:\n- Ensure all required fields (transaction_id, document_type, vendor_merchant_name, transaction_date, total_amount, currency) are present and have plausible values.\n- Check if total_amount is a positive number.\n- Assess if the line items (if present) seem consistent with the total_amount.\n- Report any inconsistencies or missing critical information."
    
    # Call the Gemini model for validation assessment
    try:
        response = aiplatform.predict.PredictionClient(client_options={"api_endpoint": f"{location}-aiplatform.googleapis.com"}).predict(
            endpoint=aiplatform.helpers.to_resource_name(project_id, location, publisher, model_id),
            instances=[predict_pb2.Instance(struct_value=json_format.ParseDict({"prompt": prompt}, predict_pb2.Instance().struct_value)).struct_value],
        )

        validation_feedback = response.predictions[0].struct_value["content"]
        
        # Based on the feedback, decide on validation status and confidence score
        validation_errors: List[str] = []
        confidence_score: float = 1.0  # Start with high confidence

        if "no inconsistencies" not in validation_feedback.lower() and "no errors" not in validation_feedback.lower():
            validation_errors.append(validation_feedback)
            confidence_score = 0.5 # Lower confidence if issues are found
        
        # Add simple programmatic checks as well
        if not normalized_expense.get("vendor_merchant_name") or normalized_expense["vendor_merchant_name"] == "Unknown":
            validation_errors.append("Vendor/Merchant name is missing or unknown.")
            confidence_score = min(confidence_score, 0.6)
        
        if not normalized_expense.get("total_amount") or normalized_expense["total_amount"] <= 0:
            validation_errors.append("Total amount is missing or not positive.")
            confidence_score = min(confidence_score, 0.4)

        # Update the normalized_expense with validation results
        normalized_expense["validation_errors"] = validation_errors
        normalized_expense["confidence_score"] = confidence_score

    except Exception as e:
        normalized_expense["validation_errors"].append(f"AI validation failed: {str(e)}")
        normalized_expense["confidence_score"] = min(normalized_expense.get("confidence_score", 1.0), 0.3)

    return normalized_expense
