from dataclasses import dataclass
from typing import Any, Dict, Mapping, Optional


@dataclass
class LoginRequest:
    state: str
    nonce: Optional[str] = None
    code_verifier: Optional[str] = None
    code_challenge: Optional[str] = None


@dataclass
class TokenResponse:
    access_token: str
    id_token: Optional[str] = None
    refresh_token: Optional[str] = None
    token_type: str = "Bearer"
    expires_in: Optional[int] = None


def normalize_profile_claims(raw: Mapping[str, Any]) -> Dict[str, Any]:
    return {
        "subject": raw.get("sub") or raw.get("id") or raw.get("user_id"),
        "email": raw.get("email") or raw.get("preferred_email"),
        "email_verified": bool(raw.get("email_verified", False)),
        "name": raw.get("name") or raw.get("display_name") or raw.get("username"),
        "given_name": raw.get("given_name"),
        "family_name": raw.get("family_name"),
        "picture": raw.get("picture") or raw.get("avatar_url"),
        "raw": dict(raw),
    }
