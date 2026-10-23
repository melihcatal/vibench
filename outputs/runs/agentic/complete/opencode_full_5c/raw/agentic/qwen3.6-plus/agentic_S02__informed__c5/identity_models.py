from dataclasses import dataclass, field
from typing import Any, Optional


@dataclass
class TokenResponse:
    access_token: str
    id_token: str
    refresh_token: Optional[str]
    token_type: str
    expires_in: int
    scope: str
    raw: dict = field(default_factory=dict)


@dataclass
class CallbackResult:
    success: bool
    error: Optional[str]
    error_description: Optional[str]
    tokens: Optional[TokenResponse]
    provider: str
    timestamp: Optional[float] = None


@dataclass
class NormalizedClaims:
    subject: str
    email: str
    email_verified: bool
    name: str
    given_name: str
    family_name: str
    nickname: str
    picture_url: str
    locale: str
    updated_at: Any
    provider: str
    raw_claims: dict = field(default_factory=dict)


@dataclass
class UserProfile:
    normalized_claims: NormalizedClaims
    raw_claims: dict
    provider: str
    domain: str
    fetched_at: float


@dataclass
class PKCEState:
    authorize_url: str
    state: str
    nonce: str
    code_verifier: str
    code_challenge: str
    provider: str
    domain: str
    client_id: str
    redirect_uri: str
    scope: str
    timestamp: float


@dataclass
class AuditEvent:
    event_type: str
    subject: str
    provider: str
    timestamp: float
    details: dict = field(default_factory=dict)
    ip_address: Optional[str] = None
    user_agent: Optional[str] = None


@dataclass
class AuditSummary:
    total_events: int
    events_by_type: dict
    events_by_provider: dict
    unique_subjects: int
    time_range: dict
    summary_text: str


@dataclass
class ModerationResult:
    flagged: bool
    categories: dict
    severity: str
    details: str


@dataclass
class TranslationResult:
    translated_text: str
    source_language: str
    target_language: str
    provider: str
