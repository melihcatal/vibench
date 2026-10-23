from dataclasses import dataclass
from typing import Optional, Dict, Any


@dataclass
class OAuthConfig:
    client_id: str
    client_secret: str
    authorization_endpoint: str
    token_endpoint: str
    userinfo_endpoint: str
    redirect_uri: str
    scope: str


@dataclass
class UserProfile:
    sub: str
    name: Optional[str] = None
    email: Optional[str] = None
    raw_claims: Optional[Dict[str, Any]] = None


@dataclass
class PKCEParams:
    code_verifier: str
    code_challenge: str
    code_challenge_method: str = "S256"


@dataclass
class AuditEvent:
    event_type: str
    user_id: str
    timestamp: str
    details: Dict[str, Any]


@dataclass
class ModerationResult:
    flagged: bool
    categories: Dict[str, bool]


@dataclass
class TranslationRequest:
    text: str
    target_language: str
    source_language: Optional[str] = None
