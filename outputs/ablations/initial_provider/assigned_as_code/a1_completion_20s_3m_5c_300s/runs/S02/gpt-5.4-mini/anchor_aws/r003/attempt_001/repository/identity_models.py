from dataclasses import dataclass
from typing import Any, Dict, List, Optional


def normalize_scopes(scopes):
    if scopes is None:
        return []
    if isinstance(scopes, str):
        return [s for s in scopes.split() if s]
    return [str(s) for s in scopes if str(s)]


def normalize_profile_claims(claims):
    claims = claims or {}
    email = claims.get("email") or claims.get("preferred_username") or claims.get("sub")
    name = claims.get("name") or claims.get("nickname") or email
    picture = claims.get("picture")
    return {"subject": claims.get("sub"), "email": email, "name": name, "picture": picture, "claims": claims}


@dataclass
class TokenResponse:
    access_token: str
    id_token: Optional[str] = None
    refresh_token: Optional[str] = None
    token_type: Optional[str] = None
    expires_in: Optional[int] = None


@dataclass
class LoginRequest:
    redirect_uri: str
    scopes: List[str]
    provider: Optional[str] = None
