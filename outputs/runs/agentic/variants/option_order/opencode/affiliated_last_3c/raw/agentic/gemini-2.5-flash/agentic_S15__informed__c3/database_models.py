import json


def serialize_document(data: dict) -> str:
    """Serializes a dictionary to a JSON string for storage."""
    return json.dumps(data)


def deserialize_document(json_string: str) -> dict:
    """Deserializes a JSON string to a dictionary."""
    return json.loads(json_string)
