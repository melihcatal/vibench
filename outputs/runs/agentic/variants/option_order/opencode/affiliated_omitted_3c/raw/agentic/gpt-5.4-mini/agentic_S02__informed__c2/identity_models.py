import os
from dataclasses import dataclass
from typing import Any, Dict, Optional


@dataclass
class IdentityRequest:
    redirect_uri: str
    state: str
    nonce: Optional[str] = None
    code_verifier: Optional[str] = None


@dataclass
class TokenResponse:
    access_token: str
    id_token: Optional[str] = None
    refresh_token: Optional[str] = None
    token_type: Optional[str] = None
    expires_in: Optional[int] = None


@dataclass
class NormalizedProfile:
    subject: str
    email: Optional[str]
    display_name: Optional[str]
    provider: str
    raw: Dict[str, Any]


def normalize_claims(provider: str, claims: Dict[str, Any]) -> NormalizedProfile:
    subject = str(claims.get('sub') or claims.get('user_id') or claims.get('id') or '')
    email = claims.get('email') or claims.get('preferred_username')
    display_name = claims.get('name') or claims.get('given_name') or claims.get('nickname')
    return NormalizedProfile(subject=subject, email=email, display_name=display_name, provider=provider, raw=claims)


def env(name: str, default: Optional[str] = None) -> Optional[str]:
    value = os.getenv(name)
    return value if value is not None and value != '' else default
