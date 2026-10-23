from typing import Any, Dict


def normalize_request(payload: Dict[str, Any]) -> Dict[str, Any]:
    return {
        "text": payload.get("text", ""),
    }


def normalize_response(response: Dict[str, Any]) -> Dict[str, Any]:
    return {
        "text": response.get("text", ""),
    }