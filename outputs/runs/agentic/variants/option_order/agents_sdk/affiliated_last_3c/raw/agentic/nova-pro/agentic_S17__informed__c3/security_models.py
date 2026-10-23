from typing import Any, Dict

def normalize_response(response: Dict[str, Any]) -> Dict[str, Any]:
    return {k: v for k, v in response.items() if v is not None}