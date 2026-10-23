from typing import Any, Dict


def normalize_payload(payload: Dict[str, Any]) -> str:
    return json.dumps(payload)


def parse_response(response: Dict[str, Any]) -> Dict[str, Any]:
    return response