import json
from typing import Dict, Any, List
from document_client import get_anthropic_client
from document_models import NormalizedExpense, ValidationResult

def validate_expense_record(expense_record: NormalizedExpense) -> ValidationResult:
    """
    Validates required structured fields and confidence scores using Anthropic Claude.
    This performs semantic validation beyond basic type/presence checks.
    """
    client = get_anthropic_client()

    record_json_str = json.dumps(expense_record, indent=2)

    prompt_content = f"""
    You are an expert at validating expense records for accuracy, consistency, and plausibility.
    Review the following normalized expense record.
    
    Check for:
    1.  **Completeness**: Are all critical fields present and non-empty (vendor_name, transaction_date, total_amount, currency, line_items)?
    2.  **Consistency**: Does the 'total_amount' roughly align with the sum of 'line_items' amounts? (Allow for minor discrepancies due to tax/rounding).
    3.  **Plausibility**: Is the 'transaction_date' a realistic date (e.g., not in the far future or distant past)? Is the 'total_amount' a reasonable value (e.g., not zero or excessively large without context)?
    4.  **Data Quality**: Are string fields like 'vendor_name' meaningful (not just empty strings or gibberish)?
    
    Respond with a JSON object containing 'is_valid' (boolean), 'reason' (string, if not valid), and 'flags' (list of strings, e.g., ["low_total_consistency", "unusual_date"]).

    Example of expected JSON response for valid:
    {{
      "is_valid": true,
      "reason": null,
      "flags": []
    }}

    Example of expected JSON response for invalid:
    {{
      "is_valid": false,
      "reason": "Total amount does not match sum of line items. Transaction date is in the future.",
      "flags": ["total_mismatch", "future_date"]
    }}

    Expense Record to Validate:
    {record_json_str}
    """

    try:
        response = client.messages.create(
            model="claude-3-haiku-20240307",
            max_tokens=500,
            messages=[
                {"role": "user", "content": prompt_content}
            ]
        )
        
        response_text = response.content[0].text
        validation_output = json.loads(response_text)

        is_valid = validation_output.get("is_valid", False)
        reason = validation_output.get("reason")
        flags = validation_output.get("flags", [])

        return ValidationResult(is_valid=is_valid, reason=reason, flags=flags)

    except json.JSONDecodeError as e:
        print(f"Failed to decode JSON from Claude response: {e}. Response: {response_text}")
        return ValidationResult(is_valid=False, reason=f"LLM response malformed: {e}", flags=["llm_response_error"])
    except Exception as e:
        print(f"Error during validation with Anthropic Claude: {e}")
        return ValidationResult(is_valid=False, reason=f"External validation service error: {e}", flags=["service_error"])
