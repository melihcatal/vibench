from typing import Dict, Any


def normalize_response(response: Dict[str, Any]) -> Dict[str, Any]:
    normalized = {}
    for key, value in response.items():
        if isinstance(value, list):
            normalized[key] = [normalize_response(item) if isinstance(item, dict) else item for item in value]
        else:
            normalized[key] = value
    return normalized