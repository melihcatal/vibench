import json
from anthropic import Anthropic
from document_client import get_anthropic_client
from document_models import NormalizedExpense, DocumentValidationResult, FieldValidation
from typing import List

def validate_expense_claude(expense: NormalizedExpense,
                            required_fields: List[str],
                            min_confidence: float = 0.7) -> DocumentValidationResult:
    """
    Validates normalized expense fields using Anthropic Claude for intelligent checks.
    It checks for required fields and assesses overall data quality.
    Requires ANTHROPIC_API_KEY environment variable.
    """
    client = get_anthropic_client()

    expense_dict = expense.model_dump(exclude_unset=True)

    prompt = f"""
    You are an expert document validator. Your task is to validate the following normalized expense data.
    The validation should include checking for the presence of required fields and evaluating the overall data quality.
    Respond with a JSON object strictly adhering to the following schema:
    {{
        "is_document_valid": boolean,
        "overall_message": "string (A brief summary of the validation outcome)",
        "field_validations": [
            {{
                "field_name": "string",
                "is_valid": boolean,
                "reason": "string (Optional, why it's invalid)",
                "confidence_score": "float (Optional, if applicable, for high confidence fields, imply 0.9, for low 0.4)"
            }}
        ],
        "required_fields_missing": ["string"],
        "low_confidence_fields": ["string"]
    }}

    The required fields for this document are: {', '.join(required_fields)}.
    Consider any field with a value as having high confidence (0.9), unless it appears malformed or is missing.
    For demonstration, any field that is None or an empty list/string should be considered missing/invalid (confidence 0.1).

    Here is the normalized expense data:
    {json.dumps(expense_dict, indent=2)}
    """

    response = client.messages.create(
        model="claude-3-opus-20240229",
        max_tokens=1024,
        messages=[
            {"role": "user", "content": prompt}
        ]
    )

    validation_result_json = response.content[0].text
    validation_dict = json.loads(validation_result_json)

    field_validations = []
    required_fields_missing = []
    low_confidence_fields = []

    for field in required_fields:
        is_present = expense_dict.get(field) is not None and expense_dict.get(field) != "" and expense_dict.get(field) != []
        if not is_present:
            required_fields_missing.append(field)
            field_validations.append(FieldValidation(
                field_name=field,
                is_valid=False,
                reason=f"Required field '{field}' is missing or empty.",
                confidence_score=0.1
            ))
        else:
            field_validations.append(FieldValidation(
                field_name=field,
                is_valid=True,
                reason=f"Required field '{field}' is present.",
                confidence_score=0.9
            ))
    
    # Add other fields reported by Claude, merging if already handled by required_fields logic
    for claude_val in validation_dict.get('field_validations', []):
        if not any(fv.field_name == claude_val['field_name'] for fv in field_validations):
            field_validations.append(FieldValidation(**claude_val))
        
        if not claude_val['is_valid'] and claude_val.get('confidence_score', 1.0) < min_confidence:
            low_confidence_fields.append(claude_val['field_name'])

    is_doc_valid = validation_dict.get('is_document_valid', True) and not required_fields_missing

    return DocumentValidationResult(
        is_document_valid=is_doc_valid,
        overall_message=validation_dict.get('overall_message', 'Validation completed.'),
        field_validations=field_validations,
        required_fields_missing=required_fields_missing,
        low_confidence_fields=low_confidence_fields
    )
