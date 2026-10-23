import json
from typing import Dict, Any


def normalize_claims(claims: Dict[str, Any]) -> Dict[str, Any]:
    # In a real application, you would map provider-specific claims to a standardized format.
    # For this example, we'll return the claims as-is.
    return {
        "sub": claims.get("sub"),
        "name": claims.get("name"),
        "email": claims.get("email"),
        "picture": claims.get("picture"),
    }


def format_audit_record(
    event_type: str, user_id: str, details: Dict[str, Any]
) -> Dict[str, Any]:
    return {
        "event_type": event_type,
        "user_id": user_id,
        "timestamp": "",  # This would be filled with current time in a real scenario
        "details": details,
    }
