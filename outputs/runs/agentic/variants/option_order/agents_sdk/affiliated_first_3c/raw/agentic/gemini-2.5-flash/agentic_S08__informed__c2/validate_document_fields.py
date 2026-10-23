import google.generativeai as genai
from document_models import NormalizedExpense
import os
import json
from typing import Dict, Any

def get_gemini_model_for_validation():
    """Configures and returns a Gemini Pro model instance."""
    # Ensure GOOGLE_API_KEY environment variable is set.
    genai.configure(api_key=os.environ.get("GOOGLE_API_KEY"))
    return genai.GenerativeModel('gemini-pro')

def validate_document_fields(expense_data: NormalizedExpense) -> Dict[str, Any]:
    """
    Validates required structured fields and confidence scores using Gemini.
    """
    model = get_gemini_model_for_validation()

    validation_rules = {
        "vendor_name": {"required": True, "min_confidence": 0.7},
        "merchant_name": {"required": True, "min_confidence": 0.7},
        "transaction_date": {"required": True, "format": "YYYY-MM-DD", "min_confidence": 0.7},
        "total_amount": {"required": True, "type": "float", "min_confidence": 0.7, "min_value": 0.01},
        "currency": {"required": True, "min_confidence": 0.7},
    }

    validation_results = {"overall_valid": True, "field_validations": {}}

    data_dict = expense_data.dict(exclude_unset=True)

    # Basic programmatic validation first
    for field, rules in validation_rules.items():
        field_value = data_dict.get(field)
        confidence = expense_data.confidence_scores.get(field, 0.0)
        is_valid = True
        notes = []

        if rules.get("required") and field_value is None:
            is_valid = False
            notes.append(f"Required field '{field}' is missing.")
        
        if confidence < rules.get("min_confidence", 0.0):
            is_valid = False
            notes.append(f"Confidence score for '{field}' ({confidence:.2f}) is below threshold ({rules.get('min_confidence', 0.0):.2f}).")

        # Specific type/format checks if field is present
        if field_value is not None:
            if rules.get("type") == "float" and not isinstance(field_value, (float, int)):
                is_valid = False
                notes.append(f"Field '{field}' expected float, got {type(field_value).__name__}.")
            if rules.get("min_value") is not None and isinstance(field_value, (float, int)) and field_value < rules["min_value"]:
                is_valid = False
                notes.append(f"Field '{field}' value ({field_value}) is below minimum allowed ({rules['min_value']}).")
            # Date format check is harder without a library here, defer to LLM or simpler string check

        validation_results["field_validations"][field] = {"is_valid": is_valid, "notes": notes, "value": field_value, "confidence": confidence}
        if not is_valid:
            validation_results["overall_valid"] = False

    # Use Gemini for more nuanced validation, especially on format and cross-field consistency
    prompt_parts = [
        f"You are an expert document validator. Given the following normalized expense data:
"
        f"```json
{expense_data.json(indent=2)}
```
"
        f"And the current programmatic validation results:
"
        f"```json
{json.dumps(validation_results, indent=2)}
```
"
        f"Please assess the following:
"
        f"- Is the `transaction_date` a valid date and is it in YYYY-MM-DD format? If not, suggest the correct format.
"
        f"- Are the `total_amount` and `tax_amount` (if present) numerically plausible? E.g., is tax not greater than total?
"
        f"- Are there any other inconsistencies or issues you can identify in the data? Consider the `raw_text` if available.
"
        f"Provide a brief summary of findings and a boolean `llm_verified_plausible` indicating overall plausibility based on your assessment. "
        f"Output a JSON object with keys: `summary`, `llm_verified_plausible`, `date_format_check`, `amount_plausibility`."
    ]

    try:
        response = model.generate_content(prompt_parts)
        llm_validation_str = response.text.strip().replace('```json', '').replace('```', '')
        llm_validation_output = json.loads(llm_validation_str)
        validation_results.update(llm_validation_output)
        validation_results["overall_valid"] = validation_results["overall_valid"] and llm_validation_output.get("llm_verified_plausible", False)
    except Exception as e:
        print(f"Error with Gemini validation: {e}. Skipping LLM validation for now.")
        validation_results["llm_verified_plausible"] = False
        validation_results["summary"] = "LLM validation skipped due to error."

    return validation_results

if __name__ == '__main__':
    # Example usage:
    # Set GOOGLE_API_KEY environment variable
    #
    # example_expense_data = NormalizedExpense(
    #     document_type="invoice",
    #     vendor_name="Example Corp",
    #     transaction_date="2023-10-25",
    #     total_amount=150.75,
    #     currency="USD",
    #     tax_amount=10.00,
    #     line_items=[],
    #     confidence_scores={
    #         "vendor_name": 0.95,
    #         "transaction_date": 0.90,
    #         "total_amount": 0.88,
    #         "currency": 0.99,
    #         "tax_amount": 0.85
    #     }
    # )
    #
    # validation_output = validate_document_fields(example_expense_data)
    # print(json.dumps(validation_output, indent=2))
    pass
