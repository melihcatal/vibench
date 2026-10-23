import jsonschema

SCHEMA = {
    "type": "object",
    "properties": {
        "expense_id": {"type": "string"},
        "merchant": {"type": "string"},
        "date": {"type": "string", "format": "date"},
        "amount": {"type": "number"},
        "line_items": {"type": "array", "items": {"type": "string"}},
        "category": {"type": "string"},
        "tax": {"type": "number"},
        "confidence": {"type": "number", "minimum": 0, "maximum": 1},
    },
    "required": ["merchant", "date", "amount", "line_items", "category", "tax", "confidence"],
    "additionalProperties": False,
}

def validate_document_fields(expense):
    '''Validate required fields and confidence score of a normalized expense record.'''
    try:
        jsonschema.validate(instance=expense, schema=SCHEMA)
    except jsonschema.ValidationError as e:
        raise ValueError(f"Invalid expense schema: {e.message}")
    if expense['confidence'] < 0.7:
        raise ValueError(f"Low confidence score {expense['confidence']}, below threshold 0.7")
    return True
