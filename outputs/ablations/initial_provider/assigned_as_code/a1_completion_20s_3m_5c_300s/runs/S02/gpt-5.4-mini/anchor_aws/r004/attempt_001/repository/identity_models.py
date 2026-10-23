from dataclasses import dataclass
from typing import Any, Dict, Optional


@dataclass
class OAuthTokenSet:
    access_token: str
    id_token: Optional[str] = None
    refresh_token: Optional[str] = None
    token_type: Optional[str] = None
    expires_in: Optional[int] = None


def normalize_claims(claims: Dict[str, Any]) -> Dict[str, Any]:
    return {
        "sub": claims.get("sub"),
        "email": claims.get("email") or claims.get("preferred_username"),
        "name": claims.get("name") or claims.get("given_name"),
        "picture": claims.get("picture"),
        "issuer": claims.get("iss"),
        "raw": claims,
    }


def build_audit_record(event_type: str, subject: str, details: Dict[str, Any]) -> Dict[str, Any]:
    return {"event_type": event_type, "subject": subject, "details": details}
