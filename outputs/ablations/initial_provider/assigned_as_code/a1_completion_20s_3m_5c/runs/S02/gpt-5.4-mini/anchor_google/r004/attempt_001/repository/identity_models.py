from dataclasses import dataclass
from typing import Any, Dict, List, Optional


@dataclass
class LoginRequest:
    redirect_uri: str
    provider_id: str
    tenant_id: Optional[str] = None


@dataclass
class TokenExchangeResult:
    access_token: str
    id_token: Optional[str] = None
    refresh_token: Optional[str] = None
    expires_in: Optional[int] = None
    token_type: Optional[str] = None


def normalize_profile_claims(claims: Dict[str, Any]) -> Dict[str, Any]:
    name = claims.get("name") or claims.get("preferred_username") or claims.get("email")
    return {
        "subject": claims.get("sub"),
        "email": claims.get("email"),
        "email_verified": bool(claims.get("email_verified")),
        "display_name": name,
        "given_name": claims.get("given_name"),
        "family_name": claims.get("family_name"),
        "picture": claims.get("picture"),
        "raw": claims,
    }


def normalize_audit_event(event: Dict[str, Any]) -> Dict[str, Any]:
    return {
        "event_type": event.get("event_type"),
        "provider": event.get("provider"),
        "subject": event.get("subject"),
        "timestamp": event.get("timestamp"),
        "details": event.get("details", {}),
    }


def coerce_scopes(scopes: Any) -> List[str]:
    if scopes is None:
        return []
    if isinstance(scopes, str):
        return [s for s in scopes.split() if s]
    return [str(scope) for scope in scopes if scope]
