from dataclasses import dataclass
from typing import Any, Dict, Optional


@dataclass
class OAuthRequest:
    client_id: str
    redirect_uri: str
    scope: str
    state: str
    code_challenge: Optional[str] = None
    code_challenge_method: Optional[str] = None


@dataclass
class OAuthTokenResponse:
    access_token: str
    id_token: Optional[str] = None
    refresh_token: Optional[str] = None
    token_type: str = "Bearer"
    expires_in: Optional[int] = None
    raw: Optional[Dict[str, Any]] = None


def normalize_google_profile(payload: Dict[str, Any]) -> Dict[str, Any]:
    return {
        "subject": payload.get("sub") or payload.get("id"),
        "email": payload.get("email"),
        "email_verified": bool(payload.get("email_verified")),
        "name": payload.get("name") or payload.get("given_name"),
        "given_name": payload.get("given_name"),
        "family_name": payload.get("family_name"),
        "picture": payload.get("picture"),
        "locale": payload.get("locale"),
        "raw": payload,
    }
