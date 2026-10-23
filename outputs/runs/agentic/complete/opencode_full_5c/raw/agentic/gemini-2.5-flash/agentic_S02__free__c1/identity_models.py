import dataclasses
from typing import Optional, Dict, Any, List


@dataclasses.dataclass
class OAuthTokens:
    access_token: str
    token_type: str
    expires_in: int
    id_token: Optional[str] = None
    refresh_token: Optional[str] = None
    scope: Optional[str] = None


@dataclasses.dataclass
class UserProfileClaims:
    sub: str  # Subject identifier
    email: Optional[str] = None
    email_verified: Optional[bool] = None
    name: Optional[str] = None
    given_name: Optional[str] = None
    family_name: Optional[str] = None
    picture: Optional[str] = None
    locale: Optional[str] = None
    hd: Optional[str] = None  # Hosted Domain for Google
    raw_claims: Dict[str, Any] = dataclasses.field(default_factory=dict)


@dataclasses.dataclass
class AuditRecord:
    timestamp: str
    event_type: str
    user_id: str
    provider: str
    details: Dict[str, Any] = dataclasses.field(default_factory=dict)


@dataclasses.dataclass
class ModerationRequest:
    text_content: str
    language_code: str = "en"


@dataclasses.dataclass
class ModerationResponse:
    moderated_content: str
    is_safe: bool
    categories: List[str]


@dataclasses.dataclass
class TranslationRequest:
    text: str
    target_language: str
    source_language: Optional[str] = None


@dataclasses.dataclass
class TranslationResponse:
    translated_text: str
    source_language: str
