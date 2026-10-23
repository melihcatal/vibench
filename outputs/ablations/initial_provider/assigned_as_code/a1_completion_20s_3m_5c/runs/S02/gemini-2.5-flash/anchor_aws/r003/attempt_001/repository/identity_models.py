from dataclasses import dataclass, field
from typing import Optional, Dict, Any, List


@dataclass
class AuthConfig:
    domain_prefix: str
    region: str
    client_id: str
    client_secret: Optional[str] = None
    redirect_uri: Optional[str] = None
    identity_provider: Optional[str] = None
    scope: str = "openid email profile"


@dataclass
class OAuthCallbackPayload:
    code: str
    state: str
    redirect_uri: str


@dataclass
class TokenResponse:
    access_token: str
    id_token: Optional[str] = None
    refresh_token: Optional[str] = None
    expires_in: int = 3600
    token_type: str = "Bearer"


@dataclass
class UserProfileClaims:
    sub: str
    email: Optional[str] = None
    email_verified: Optional[bool] = None
    name: Optional[str] = None
    picture: Optional[str] = None
    # Add other common claims as needed
    raw_claims: Dict[str, Any] = field(default_factory=dict)


@dataclass
class PKCEPayload:
    code_verifier: str
    redirect_uri: str
    code: str


@dataclass
class AuditRecord:
    event_type: str
    user_id: Optional[str] = None
    timestamp: str
    details: Dict[str, Any] = field(default_factory=dict)


@dataclass
class TranslatedConsent:
    original_text: str
    translated_text: str
    target_language: str


@dataclass
class ClaimModerationResult:
    original_claim: str
    moderated_claim: str
    sentiment_score: Optional[float] = None
    moderation_flags: List[str] = field(default_factory=list)
