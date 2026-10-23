import dataclasses
from typing import Any, Dict, Mapping, Optional

@dataclasses.dataclass
class LoginRequest:
    redirect_uri: str
    state: str
    code_verifier: Optional[str] = None
    nonce: Optional[str] = None

@dataclasses.dataclass
class TokenResponse:
    access_token: str
    id_token: Optional[str] = None
    refresh_token: Optional[str] = None
    expires_in: Optional[int] = None
    token_type: Optional[str] = None
    raw: Optional[Dict[str, Any]] = None

@dataclasses.dataclass
class ProfileClaims:
    subject: str
    email: Optional[str]
    display_name: Optional[str]
    issuer: Optional[str]
    raw: Dict[str, Any]

def normalize_claims(claims: Mapping[str, Any]) -> ProfileClaims:
    subject = str(claims.get('sub') or claims.get('id') or claims.get('user_id') or '')
    email = claims.get('email') or claims.get('preferred_username')
    display_name = claims.get('name') or claims.get('given_name') or claims.get('nickname')
    issuer = claims.get('iss') or claims.get('issuer')
    return ProfileClaims(subject=subject, email=email, display_name=display_name, issuer=issuer, raw=dict(claims))
