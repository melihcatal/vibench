from document_client import get_cohere_client
from document_models import NormalizedExpense
from typing import Dict, Any

def validate_document_fields(expense: NormalizedExpense) -> Dict[str, Any]:
    client = get_cohere_client()

    validation_rules = [
        "vendor_name must not be empty.",
        "transaction_date must be a valid date.",
        "total_amount must be a positive number.",
        "document_type must be either 'invoice' or 'receipt'."
    ]

    # Basic structural validation first
    is_valid = True
    issues = []

    if not expense.vendor_name:
        is_valid = False
        issues.append("Vendor name is missing.")
    if not isinstance(expense.transaction_date, date):
        is_valid = False
        issues.append("Transaction date is invalid or missing.")
    if expense.total_amount <= 0:
        is_valid = False
        issues.append("Total amount must be positive.")
    if expense.document_type not in ["invoice", "receipt"]:
        is_valid = False
        issues.append("Document type must be 'invoice' or 'receipt'.")

    # Use Cohere for more sophisticated semantic validation or confidence assessment
    prompt = f"""Review the following normalized expense record for completeness, accuracy, and adherence to common expense reporting standards. 
               Provide a concise validation summary, including any identified issues. 
               If all required fields are present and appear reasonable, assign a high confidence score (0.8-1.0), otherwise a lower score.
               
               Normalized Expense Record:
               {expense.model_dump_json(indent=2)}
               
               Required fields for high confidence: vendor_name, transaction_date, total_amount, currency.
               
               Return a JSON object with 'validation_summary' (string), 'is_valid' (boolean), and 'confidence_score' (float).
            """

    response = client.chat(
        model="command-r-plus", # Concrete model identifier
        message=prompt,
        response_type="json",
        temperature=0.0
    )

    cohere_validation_output = response.text
    try:
        cohere_result = json.loads(cohere_validation_output)
    except json.JSONDecodeError:
        cohere_result = {
            "validation_summary": f"Cohere failed to return valid JSON: {cohere_validation_output}",
            "is_valid": False,
            "confidence_score": 0.0
        }

    # Combine local validation with Cohere's assessment
    final_is_valid = is_valid and cohere_result.get("is_valid", False)
    final_summary_lines = issues + [cohere_result.get("validation_summary", "")]
    final_summary = ". ".join(filter(None, final_summary_lines))
    final_confidence = cohere_result.get("confidence_score", 0.0) # Use Cohere's score if available

    return {
        "is_valid": final_is_valid,
        "validation_summary": final_summary,
        "confidence_score": final_confidence
    }
