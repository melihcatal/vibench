from dataclasses import dataclass
from typing import Any, Dict, Optional


@dataclass
class OAuthLoginRequest:
    redirect_uri: str
    state: str
    nonce: Optional[str] = None
    scope: str = "openid email profile"


@dataclass
class OAuthTokenResponse:
    access_token: str
    id_token: Optional[str] = None
    refresh_token: Optional[str] = None
    token_type: Optional[str] = None
    expires_in: Optional[int] = None


def normalize_claims(payload: Dict[str, Any]) -> Dict[str, Any]:
    email = payload.get("email") or payload.get("preferred_username")
    name = payload.get("name") or payload.get("given_name") or email
    return {
        "subject": payload.get("sub") or payload.get("user_id") or "",
        "email": email or "",
        "name": name or "",
        "picture": payload.get("picture") or payload.get("avatar_url") or "",
        "provider": payload.get("iss") or payload.get("provider") or "google",
        "raw": payload,
    }
