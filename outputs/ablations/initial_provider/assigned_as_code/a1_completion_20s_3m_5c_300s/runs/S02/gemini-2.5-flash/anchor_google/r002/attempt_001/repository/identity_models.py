from dataclasses import dataclass, field
from typing import Dict, Any, List

@dataclass
class TokenExchangeRequest:
    code: str
    redirect_uri: str
    client_id: str
    client_secret: str = field(default=None)
    code_verifier: str = field(default=None)

@dataclass
class TokenExchangeResponse:
    access_token: str
    id_token: str
    token_type: str
    expires_in: int
    refresh_token: str = field(default=None)

@dataclass
class ProfileClaims:
    sub: str
    email: str = field(default=None)
    email_verified: bool = field(default=None)
    name: str = field(default=None)
    given_name: str = field(default=None)
    family_name: str = field(default=None)
    picture: str = field(default=None)
    locale: str = field(default=None)
    normalized_claims: Dict[str, Any] = field(default_factory=dict)

@dataclass
class AuditRecord:
    event_type: str
    timestamp: str
    user_id: str
    provider_id: str
    details: Dict[str, Any]

@dataclass
class ModerationResult:
    original_text: str
    moderated_text: str
    is_flagged: bool
    reasons: List[str]

@dataclass
class TranslationRequest:
    text: str
    target_language: str
    source_language: str = field(default=None)

@dataclass
class TranslationResult:
    original_text: str
    translated_text: str
    source_language: str
    target_language: str
