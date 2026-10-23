from typing import Any, Dict


def normalize_response(response: Dict[str, Any]) -> str:
    return response["text"]
