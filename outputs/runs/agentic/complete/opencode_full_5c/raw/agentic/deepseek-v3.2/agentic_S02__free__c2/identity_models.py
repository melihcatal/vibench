from dataclasses import dataclass, field
from typing import Dict, Any, List, Optional
from datetime import datetime


@dataclass
class OAuthStartRequest:
    redirect_uri: str
    scopes: List[str] = field(default_factory=lambda: ["openid", "email", "profile"])
    use_oidc: bool = True


@dataclass
class OAuthStartResponse:
    authorization_url: str
    state: str
    nonce: Optional[str]
    provider: str


@dataclass
class OAuthCallbackRequest:
    code: str
    state: str


@dataclass
class OAuthCallbackResponse:
    access_token: str
    refresh_token: Optional[str]
    id_token: Optional[str]
    expires_in: int
    token_type: str
    scope: str
    provider: str


@dataclass
class ProfileRequest:
    access_token: Optional[str] = None
    id_token: Optional[str] = None


@dataclass
class NormalizedProfile:
    subject: str
    email: str
    email_verified: bool
    name: str
    given_name: str
    family_name: str
    picture: str
    locale: str
    provider: str
    raw_claims: Dict[str, Any]


@dataclass
class PKCELoginRequest:
    redirect_uri: str
    scopes: List[str] = field(default_factory=lambda: ["openid", "email", "profile"])
    use_oidc: bool = True


@dataclass
class PKCELoginResponse:
    authorization_url: str
    state: str
    code_verifier: str
    code_challenge: str
    nonce: Optional[str]
    provider: str


@dataclass
class AuditEvent:
    event_id: str
    timestamp: datetime
    user_id: str
    provider: str
    event_type: str
    details: Dict[str, Any]
    ip_address: Optional[str] = None
    user_agent: Optional[str] = None


@dataclass
class ModerationRequest:
    text: str
    content_type: str = "profile_note"


@dataclass
class ModerationResponse:
    is_approved: bool
    categories: Dict[str, float]
    flagged: bool
    provider: str


@dataclass
class TranslationRequest:
    text: str
    target_language: str
    source_language: Optional[str] = None


@dataclass
class TranslationResponse:
    translated_text: str
    source_language: str
    target_language: str
    provider: str
