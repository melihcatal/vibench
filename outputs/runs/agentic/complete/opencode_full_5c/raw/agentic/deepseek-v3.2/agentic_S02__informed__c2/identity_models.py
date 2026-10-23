from dataclasses import dataclass
from typing import Optional, Dict, Any
from datetime import datetime


@dataclass
class TokenResponse:
    """OAuth/OIDC token response."""

    access_token: str
    id_token: Optional[str] = None
    refresh_token: Optional[str] = None
    token_type: Optional[str] = "Bearer"
    expires_in: Optional[int] = None
    scope: Optional[str] = None


@dataclass
class UserProfile:
    """User profile from identity provider."""

    sub: str
    email: Optional[str] = None
    email_verified: Optional[bool] = None
    name: Optional[str] = None
    given_name: Optional[str] = None
    family_name: Optional[str] = None
    nickname: Optional[str] = None
    picture: Optional[str] = None
    locale: Optional[str] = None
    updated_at: Optional[str] = None


@dataclass
class NormalizedClaims:
    """Normalized user claims in standard format."""

    user_id: str
    email: Optional[str]
    email_verified: Optional[bool]
    full_name: Optional[str]
    first_name: Optional[str]
    last_name: Optional[str]
    display_name: Optional[str]
    avatar_url: Optional[str]
    locale: Optional[str]
    provider: str
    raw_claims: Dict[str, Any]


@dataclass
class AuthError(Exception):
    """Authentication error."""

    message: str
    error_code: Optional[str] = None
    error_description: Optional[str] = None

    def __str__(self):
        return self.message


@dataclass
class LoginRequest:
    """Login request parameters."""

    redirect_uri: str
    state: Optional[str] = None
    nonce: Optional[str] = None
    scope: Optional[str] = "openid profile email"
    prompt: Optional[str] = None


@dataclass
class CallbackRequest:
    """OAuth callback request parameters."""

    code: str
    state: str
    redirect_uri: str
    error: Optional[str] = None
    error_description: Optional[str] = None


@dataclass
class LoginResult:
    """Login result."""

    success: bool
    user: Optional[NormalizedClaims] = None
    tokens: Optional[TokenResponse] = None
    error: Optional[AuthError] = None
    redirect_url: Optional[str] = None


@dataclass
class AuditEvent:
    """Login audit event."""

    event_id: str
    timestamp: datetime
    user_id: Optional[str]
    provider: str
    event_type: str
    ip_address: Optional[str] = None
    user_agent: Optional[str] = None
    success: bool = True
    details: Optional[Dict[str, Any]] = None


@dataclass
class ModerationResult:
    """Content moderation result."""

    approved: bool
    score: Optional[float] = None
    categories: Optional[Dict[str, float]] = None
    reasons: Optional[list[str]] = None
    moderated_text: Optional[str] = None


@dataclass
class TranslationResult:
    """Translation result."""

    translated_text: str
    source_language: str
    target_language: str
    detected_language: Optional[str] = None
    confidence: Optional[float] = None
