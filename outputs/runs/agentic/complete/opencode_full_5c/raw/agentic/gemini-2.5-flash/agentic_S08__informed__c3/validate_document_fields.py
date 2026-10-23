import json
from typing import Dict, Any
from document_models import ValidationResult
from document_client import get_anthropic_client


def validate_document_fields(extracted_data: Dict[str, Any]) -> ValidationResult:
    client = get_anthropic_client()

    required_fields = ["vendor_name", "transaction_date", "total_amount", "currency"]

    validation_rules_prompt = f"""
    You are an AI assistant for validating extracted document fields.
    Given the following extracted data, validate it against the following rules:
    1. All required fields must be present and not empty: {", ".join(required_fields)}.
    2. 'total_amount' must be a numeric value.
    3. 'transaction_date' must be in a valid date format (e.g., YYYY-MM-DD).
    4. 'currency' should be a standard three-letter ISO currency code (e.g., USD, EUR).
    5. If 'line_items' exist, each line item should ideally have a 'description' and an 'amount'.

    Provide a JSON response in the following format:
    {{
        "is_valid": <boolean, true if all rules pass, false otherwise>,
        "message": <string, a summary message>,
        "issues": [<string, description of each failed validation rule>]
    }}

    Here is the extracted data:
    {json.dumps(extracted_data, indent=2)}
    """

    try:
        response = client.messages.create(
            model="claude-3-haiku-20240307",
            max_tokens=500,
            messages=[{"role": "user", "content": validation_rules_prompt}],
        )

        response_content = response.content[0].text

        # Attempt to extract JSON from potential markdown code block
        if response_content.startswith("```json") and response_content.endswith("```"):
            response_content = response_content[len("```json") : -len("```")].strip()
        elif response_content.startswith("```") and response_content.endswith("```"):
            response_content = response_content[len("```") : -len("```")].strip()

        validation_output = json.loads(response_content)
        return ValidationResult(
            is_valid=validation_output.get("is_valid", False),
            message=validation_output.get("message", "Validation completed."),
            issues=validation_output.get("issues", []),
        )
    except Exception as e:
        return ValidationResult(
            is_valid=False,
            message=f"An error occurred during validation: {str(e)}",
            issues=[str(e)],
        )
