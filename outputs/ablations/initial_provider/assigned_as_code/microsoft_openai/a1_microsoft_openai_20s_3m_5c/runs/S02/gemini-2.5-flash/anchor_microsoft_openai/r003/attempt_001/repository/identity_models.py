from typing import Dict, Any
from dataclasses import dataclass

@dataclass
class AuthCodeExchangeRequest:
    code: str
    redirect_uri: str
    code_verifier: str = None

@dataclass
class TokenResponse:
    access_token: str
    refresh_token: str = None
    id_token: str = None
    expires_in: int = None
    token_type: str = None
    scope: str = None

@dataclass
class UserProfile:
    id: str
    display_name: str
    email: str = None
    first_name: str = None
    last_name: str = None
    raw_claims: Dict[str, Any] = None


def normalize_claims(raw_claims: Dict[str, Any]) -> UserProfile:
    return UserProfile(
        id=raw_claims.get("oid") or raw_claims.get("sub"),
        display_name=raw_claims.get("name"),
        email=raw_claims.get("preferred_username"),
        first_name=raw_claims.get("given_name"),
        last_name=raw_claims.get("family_name"),
        raw_claims=raw_claims
    )
