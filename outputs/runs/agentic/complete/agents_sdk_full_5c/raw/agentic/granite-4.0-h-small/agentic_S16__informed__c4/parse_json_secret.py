import json
from typing import Any, Dict

def parse_json_secret(secret_value: str) -> Dict[str, Any]:
    """Parse a JSON-formatted secret value and return a dict.

    Args:
        secret_value: Raw JSON string stored in a secret.

    Returns:
        Dictionary representation of the JSON.
    """
    try:
        data = json.loads(secret_value)
        if not isinstance(data, dict):
            raise ValueError("Secret must contain a JSON object at the top level")
        return data
    except json.JSONDecodeError as exc:
        raise ValueError(f"Invalid JSON secret: {exc}") from exc
