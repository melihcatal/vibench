from cerberus import Validator
from typing import Dict, Any, List


def validate_extracted_fields(
    extracted_data: Dict[str, Any], confidence_scores: Dict[str, float]
) -> List[str]:
    """Validates extracted document fields and confidence scores."""
    schema = {
        "vendor": {"type": "string", "required": True, "minlength": 1},
        "transaction_date": {
            "type": "string",
            "required": True,
            "regex": r"\d{4}-\d{2}-\d{2}",
        },
        "total": {"type": "float", "required": True, "min": 0},
        "items": {
            "type": "list",
            "required": True,
            "schema": {
                "type": "dict",
                "schema": {
                    "description": {"type": "string", "required": True, "minlength": 1},
                    "amount": {"type": "float", "required": True, "min": 0},
                },
            },
        },
    }

    validator = Validator(schema)
    errors = []

    if not validator.validate(extracted_data):
        errors.extend([f"Field '{k}': {v[0]}" for k, v in validator.errors.items()])

    for field, score in confidence_scores.items():
        if score < 0.85:
            errors.append(f"Low confidence score for field '{field}': {score:.2f}")

    return errors
