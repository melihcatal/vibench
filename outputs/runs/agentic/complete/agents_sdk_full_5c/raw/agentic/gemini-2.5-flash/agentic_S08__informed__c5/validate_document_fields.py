import os
import json
import google.generativeai as genai

def validate_expense_fields(normalized_expense: dict, required_fields: list, min_confidence: float = 0.7) -> dict:
    """
    Validates required structured fields and confidence scores using Google Gemini API for semantic checks.
    For demonstration, we'll perform basic structural validation and then use Gemini for semantic validation.
    """
    genai.configure(api_key=os.environ.get("GOOGLE_API_KEY"))
    model = genai.GenerativeModel('gemini-pro')

    validation_report = {
        "is_valid": True,
        "missing_required_fields": [],
        "fields_below_min_confidence": [], # Placeholder, assuming confidence scores are part of normalized_expense if available
        "semantic_validation_issues": [],
        "original_data": normalized_expense
    }

    # 1. Check for required fields (structural validation)
    for field in required_fields:
        if field not in normalized_expense or not normalized_expense[field]:
            validation_report["is_valid"] = False
            validation_report["missing_required_fields"].append(field)
    
    # 2. Semantic validation using LLM
    # This part can be expanded for more complex checks, e.g., date formats, total consistency
    prompt = f"""Review the following normalized expense data and identify any potential inconsistencies, anomalies, or values that seem incorrect based on common expense reporting standards. Focus on semantic correctness rather than just structural presence.\n\nNormalized Expense Data:\n{json.dumps(normalized_expense, indent=2)}\n\nReturn a JSON array of identified issues. If no issues, return an empty array. Each issue should be an object with 'field', 'issue_type', and 'description'."""

    try:
        response = model.generate_content(prompt)
        semantic_issues_str = response.text.strip()
        semantic_issues = json.loads(semantic_issues_str)
        if semantic_issues:
            validation_report["is_valid"] = False
            validation_report["semantic_validation_issues"] = semantic_issues
    except Exception as e:
        print(f"Error during semantic validation with Gemini API: {e}")
        validation_report["is_valid"] = False
        validation_report["semantic_validation_issues"].append({
            "field": "overall",
            "issue_type": "LLM_API_ERROR",
            "description": f"Failed to perform semantic validation: {str(e)}"
        })

    # Placeholder for confidence score validation, assuming scores are embedded in normalized_expense
    # if normalized_expense.get("confidence_scores"):
    #     for field, score in normalized_expense["confidence_scores"].items():
    #         if score < min_confidence:
    #             validation_report["is_valid"] = False
    #             validation_report["fields_below_min_confidence"].append(f"{field} (score: {score})")

    return validation_report

if __name__ == '__main__':
    sample_normalized_expense = {
        "expense_type": "invoice",
        "date": "2023-10-26",
        "vendor_name": "Acme Corp",
        "total_amount": 125.50,
        "currency": "USD",
        "tax_amount": 0.0,
        "line_items": [
            {"description": "Consulting Services", "quantity": 1, "unit_price": 100.00, "total_price": 100.00},
            {"description": "Travel Expenses", "quantity": 1, "unit_price": 25.50, "total_price": 25.50}
        ]
    }

    required_fields_list = ["date", "vendor_name", "total_amount"]

    if not os.environ.get("GOOGLE_API_KEY"):
        print("Please set GOOGLE_API_KEY environment variable.")
    else:
        print("Validating sample normalized expense data...")
        validation_result = validate_expense_fields(sample_normalized_expense, required_fields_list)
        print("Validation Report:", json.dumps(validation_result, indent=2))

        # Example with missing data and potential semantic issue (e.g., negative total)
        invalid_sample = sample_normalized_expense.copy()
        invalid_sample["total_amount"] = -50.00 # Semantic issue
        del invalid_sample["vendor_name"] # Missing required field

        print("\nValidating invalid sample data...")
        invalid_validation_result = validate_expense_fields(invalid_sample, required_fields_list)
        print("Invalid Validation Report:", json.dumps(invalid_validation_result, indent=2))
