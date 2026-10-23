import json


def parse_json_secret(secret_value: str) -> dict:
    """Parse a raw JSON-formatted secret string into a Python dict.

    Args:
        secret_value (str): Raw secret value as JSON.

    Returns:
        dict: Parsed JSON data.
    """
    return json.loads(secret_value)
