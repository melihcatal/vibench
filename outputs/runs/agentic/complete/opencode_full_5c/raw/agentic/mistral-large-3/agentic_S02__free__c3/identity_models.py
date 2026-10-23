from dataclasses import dataclass
from typing import Optional, Dict, Any


@dataclass
class ProfileClaims:
    sub: Optional[str] = None
    name: Optional[str] = None
    given_name: Optional[str] = None
    family_name: Optional[str] = None
    email: Optional[str] = None
    email_verified: Optional[bool] = False
    picture: Optional[str] = None
    locale: Optional[str] = None
    updated_at: Optional[str] = None


@dataclass
class OAuthConfig:
    domain: str
    client_id: str
    client_secret: Optional[str] = None
    callback_url: Optional[str] = None
    audience: Optional[str] = None
    scope: Optional[str] = None


@dataclass
class PKCERequest:
    code_verifier: str
    code_challenge: str


@dataclass
class TokenResponse:
    access_token: str
    id_token: str
    refresh_token: Optional[str] = None
    expires_in: Optional[int] = None


@dataclass
class AuditEvent:
    event_id: str
    user_id: str
    event_type: str
    timestamp: str
    metadata: Dict[str, Any]


@dataclass
class ConsentTranslation:
    provider_text: str
    translated_text: str
    locale: str
