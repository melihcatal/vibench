from typing import Dict, Any, Union

# Placeholder for more complex models if needed
# For now, we'll use basic Python types.

SecretValue = Union[str, bytes, Dict[str, Any]]

def normalize_secret_value(value: Union[str, bytes]) -> str:
    """
    Normalizes a secret value to a string.
    """
    if isinstance(value, bytes):
        return value.decode("utf-8")
    return value

def parse_json_string_to_dict(json_string: str) -> Dict[str, Any]:
    """
    Parses a JSON string into a dictionary.
    """
    import json
    return json.loads(json_string)
