import json
from document_client import get_gemini_client
from document_models import NormalizedExpense, FieldValidationResult
import google.generativeai as genai
from typing import List


def validate_document_fields(expense: NormalizedExpense) -> List[FieldValidationResult]:
    model = get_gemini_client()

    required_fields = [
        ("vendor_name", expense.vendor_name),
        ("transaction_date", expense.transaction_date),
        ("total_amount", expense.total_amount),
        ("currency", expense.currency),
    ]

    validation_results = []

    for field_name, field_value in required_fields:
        if field_value is None:
            validation_results.append(
                FieldValidationResult(
                    field_name=field_name,
                    is_valid=False,
                    reason=f"{field_name} is missing.",
                )
            )
        else:
            validation_results.append(
                FieldValidationResult(field_name=field_name, is_valid=True, reason=None)
            )

    # Example of LLM-based validation for more complex rules or semantic checks
    prompt = f"""
    Review the following normalized expense record and provide a concise validation summary.
    Specifically, check if the total_amount is a positive number and if the transaction_date is in a reasonable format (YYYY-MM-DD or similar).
    If line_items are present, check if their total prices sum up approximately to the total_amount, allowing for minor discrepancies.
    
    Normalized Expense Record:
    {json.dumps(expense.dict(), indent=2)}
    
    Provide the output as a JSON list of validation results, similar to the FieldValidationResult schema.
    Example: [
        {{"field_name": "total_amount", "is_valid": true, "reason": null}},
        {{"field_name": "transaction_date", "is_valid": false, "reason": "Invalid date format."}}
    ]
    """

    response = model.generate_content(prompt)
    try:
        llm_validation_output = json.loads(
            response.text.strip().replace("```json", "").replace("```", "")
        )
        for item in llm_validation_output:
            validation_results.append(FieldValidationResult(**item))
    except (json.JSONDecodeError, KeyError, TypeError) as e:
        print(f"Warning: Gemini validation output parsing failed. Error: {e}")
        validation_results.append(
            FieldValidationResult(
                field_name="llm_validation",
                is_valid=False,
                reason=f"Failed to parse LLM validation response: {e}",
            )
        )

    return validation_results
