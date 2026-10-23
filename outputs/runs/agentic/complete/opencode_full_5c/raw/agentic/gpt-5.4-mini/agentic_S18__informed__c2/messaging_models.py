import json
from typing import Any, Dict, Optional


def normalize_payload(payload: Any) -> Any:
    if isinstance(payload, str):
        try:
            return json.loads(payload)
        except json.JSONDecodeError:
            return {"text": payload}
    return payload


def normalize_attributes(attributes: Optional[Dict[str, Any]]) -> Dict[str, Dict[str, str]]:
    result: Dict[str, Dict[str, str]] = {}
    if not attributes:
        return result
    for key, value in attributes.items():
        result[key] = {"DataType": "String", "StringValue": str(value)}
    return result


def make_message_record(provider: str, action: str, message_id: Optional[str], status: str, payload: Any = None, details: Any = None) -> Dict[str, Any]:
    return {"provider": provider, "action": action, "message_id": message_id, "status": status, "payload": payload, "details": details}
