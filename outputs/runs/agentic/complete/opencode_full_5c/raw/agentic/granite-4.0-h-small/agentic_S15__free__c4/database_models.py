# [HELPER] database_models.py
"""Local helpers for request/response normalization for the DynamoDB NoSQL document store.

Provides utilities to transform between incoming JSON payloads and DynamoDB
attribute structures, as well as to extract and normalize query results into
plain Python `dict` objects.
"""

from typing import Any, Dict


def normalize_request(document: Dict[str, Any]) -> Dict[str, Dict[str, Any]]:
    """Convert a plain dict to DynamoDB AttributeValue format.

    DynamoDB expects values to be wrapped, e.g., {'S': 'value'} for strings,
    {'N': '123'} for numbers, {'BOOL': True} for booleans, etc.
    """
    normalized = {}
    for key, value in document.items():
        if isinstance(value, str):
            normalized[key] = {"S": value}
        elif isinstance(value, (int, float)):
            # Store numbers as strings to avoid DynamoDB treating them as sets
            normalized[key] = {"N": str(value)}
        elif isinstance(value, bool):
            normalized[key] = {"BOOL": value}
        elif isinstance(value, list):
            # Convert list items to appropriate AttributeValues
            normalized[key] = {
                "L": [normalize_request({"dummy": v})["dummy"] for v in value]
            }
        elif value is None:
            normalized[key] = {"NULL": True}
        else:
            # Fallback: store as a JSON string
            normalized[key] = {"S": str(value)}
    return normalized


def normalize_response(item: Dict[str, Any]) -> Dict[str, Any]:
    """Convert a DynamoDB item (AttributeValue dict) back to plain Python types.

    Handles the most common types: string, number, boolean, list, and null.
    """

    def convert(val):
        dtype = list(val.keys())[0]
        value = val[dtype]
        if dtype == "S":
            return value
        elif dtype == "N":
            return float(value)  # keep as float for simplicity
        elif dtype == "BOOL":
            return value
        elif dtype == "NULL":
            return None
        elif dtype == "L":
            return [convert(item) for item in value]
        elif dtype == "M":
            # Nested map: recursively normalize
            return {k: convert(v) for k, v in value.items()}
        else:
            # Fallback to string representation
            return str(val)

    return {k: convert(v) for k, v in item.items()}
