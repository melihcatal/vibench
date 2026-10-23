from typing import Dict, Any


def normalize_payload(payload: Dict[str, Any]) -> Dict[str, Any]:
    return {
        "email": payload.get("email"),
        "password": payload.get("password"),
    }