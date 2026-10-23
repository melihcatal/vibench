from typing import Dict, Any


def normalize_response(response: Dict[str, Any]) -> str:
    return response["text"]


def parse_response(response: Dict[str, Any]) -> Dict[str, Any]:
    return response
