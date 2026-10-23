from dataclasses import dataclass, field
from typing import Optional, Dict, Any


@dataclass
class TokenResponse:
    access_token: str
    id_token: Optional[str] = None
    expires_in: Optional[int] = None
    token_type: Optional[str] = None
    scope: Optional[str] = None


@dataclass
class UserProfile:
    sub: str
    name: Optional[str] = None
    email: Optional[str] = None
    email_verified: Optional[bool] = None
    picture: Optional[str] = None
    given_name: Optional[str] = None
    family_name: Optional[str] = None
    locale: Optional[str] = None
    # Add any other common claims you expect
    raw_claims: Dict[str, Any] = field(default_factory=dict)


@dataclass
class AuditEvent:
    event_id: str
    timestamp: str
    user_id: str
    event_type: str
    details: Dict[str, Any]


@dataclass
class ModerationResult:
    text: str
    is_toxic: bool
    scores: Dict[str, float]


@dataclass
class TranslationResult:
    original_text: str
    translated_text: str
    source_language: str
    target_language: str
