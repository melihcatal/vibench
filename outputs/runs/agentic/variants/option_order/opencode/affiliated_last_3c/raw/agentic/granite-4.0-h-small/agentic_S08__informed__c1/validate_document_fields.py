import json


def validate_document_fields(data: dict, required: list) -> bool:
    """Validate that required fields exist and confidence scores meet a threshold."""
    missing = [field for field in required if field not in data or not data[field]]
    if missing:
        raise ValueError(f"Missing required fields: {', '.join(missing)}")
    # Assume confidence score stored under 'confidence' key for each field
    for field, value in data.items():
        if (
            isinstance(value, dict)
            and "confidence" in value
            and value["confidence"] < 0.8
        ):
            raise ValueError(f"Low confidence {field}: {value['confidence']}")
    return True


if __name__ == "__main__":
    sample = {
        "vendor": "Acme Corp",
        "date": "2024-07-15",
        "total": 135.0,
        "line_items": [
            {
                "description": "Widget",
                "quantity": 2,
                "unit_price": 10.0,
                "total": 20.0,
                "confidence": 0.92,
            }
        ],
    }
    required_fields = ["vendor", "date", "total", "line_items"]
    try:
        if validate_document_fields(sample, required_fields):
            print("Document fields valid")
    except ValueError as e:
        print(e)
