import os
import cohere
from typing import Dict, Any, List

from document_models import ValidationResult

def validate_document_fields(
    extracted_data: Dict[str, Any],
    required_fields: List[str],
    min_confidence: float = 0.85
) -> ValidationResult:
    """
    Validates extracted document fields using Cohere.
    """
    api_key = os.environ.get("COHERE_API_KEY")
    co = cohere.Client(api_key)

    prompt = f"""
    Validate the following extracted data from a document based on two rules:
    1. All required fields must be present and not empty.
    2. The confidence score for each field must be above the minimum threshold.

    Extracted Data with Confidence Scores:
    {extracted_data}

    Required Fields:
    {required_fields}

    Minimum Confidence Threshold:
    {min_confidence}

    Return a JSON object with two keys:
    - "is_valid": boolean, true if all rules pass, otherwise false.
    - "errors": a list of strings describing each validation failure.
    
    Example response for failure:
    {{
      "is_valid": false,
      "errors": ["Missing required field: 'total'", "Field 'date' has low confidence: 0.78"]
    }}
    
    Example response for success:
    {{
      "is_valid": true,
      "errors": []
    }}
    """

    response = co.chat(
        model="command-r",
        message=prompt,
        temperature=0.0
    )

    try:
        # Assuming the model returns a JSON string in its response
        validation_json = response.text
        result_data = eval(validation_json) # Using eval for simplicity; json.loads preferred in prod
        return ValidationResult(**result_data)
    except Exception as e:
        return ValidationResult(
            is_valid=False,
            errors=[f"Failed to parse validation response: {e}"]
        )
