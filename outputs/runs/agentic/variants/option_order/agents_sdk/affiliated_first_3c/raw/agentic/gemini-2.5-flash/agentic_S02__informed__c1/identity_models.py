from typing import Dict, Any, Optional
from dataclasses import dataclass, field

@dataclass
class AuthCodeRequest:
    authorization_code: str
    redirect_uri: str
    code_verifier: Optional[str] = None
    state: Optional[str] = None

@dataclass
class TokenResponse:
    access_token: str
    token_type: str
    expires_in: int
    id_token: Optional[str] = None
    refresh_token: Optional[str] = None
    scope: Optional[str] = None

@dataclass
class UserProfileClaims:
    provider: str
    id: str
    email: Optional[str] = None
    email_verified: Optional[bool] = None
    name: Optional[str] = None
    given_name: Optional[str] = None
    family_name: Optional[str] = None
    picture: Optional[str] = None
    locale: Optional[str] = None
    raw_claims: Dict[str, Any] = field(default_factory=dict)

    @classmethod
    def from_google_claims(cls, claims: Dict[str, Any]):
        return cls(
            provider="google",
            id=claims.get("sub", ""),
            email=claims.get("email"),
            email_verified=claims.get("email_verified"),
            name=claims.get("name"),
            given_name=claims.get("given_name"),
            family_name=claims.get("family_name"),
            picture=claims.get("picture"),
            locale=claims.get("locale"),
            raw_claims=claims
        )

@dataclass
class AuditEvent:
    event_id: str
    timestamp: str
    user_id: str
    event_type: str # e.g., 'login_success', 'login_failure'
    ip_address: str
    user_agent: str
    details: Dict[str, Any] = field(default_factory=dict)


@dataclass
class ModerationResult:
    flagged: bool
    score: float
    reason: str
    provider: str

@dataclass
class TranslationResult:
    translated_text: str
    source_language: str
    target_language: str
    provider: str
