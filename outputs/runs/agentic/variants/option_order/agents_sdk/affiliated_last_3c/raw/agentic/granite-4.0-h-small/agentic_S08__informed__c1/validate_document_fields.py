import json

def validate_document_fields(data: dict, required_fields: list) -> bool:
    missing = [field for field in required_fields if field not in data or data[field] is None]
    if missing:
        print(f"Missing required fields: {missing}")
        return False
    if 'confidence' not in data or not (0 <= data['confidence'] <= 1):
        print('Missing or invalid confidence score')
        return False
    return True
