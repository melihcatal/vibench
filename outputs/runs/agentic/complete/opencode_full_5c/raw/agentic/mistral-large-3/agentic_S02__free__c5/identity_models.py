from typing import Dict, Optional, List
from dataclasses import dataclass
from datetime import datetime


@dataclass
class OAuthStartResponse:
    authorization_url: str
    state: str
    provider: str
    model_id: str
    pkce_data: Optional["PKCEData"] = None


@dataclass
class PKCEData:
    code_verifier: str
    code_challenge: str


@dataclass
class TokenResponse:
    access_token: str
    refresh_token: Optional[str]
    id_token: Optional[str]
    expires_in: Optional[int]
    token_type: str
    provider: str
    model_id: str


@dataclass
class ProfileClaims:
    sub: str
    name: Optional[str] = None
    given_name: Optional[str] = None
    family_name: Optional[str] = None
    email: Optional[str] = None
    email_verified: Optional[bool] = None
    picture: Optional[str] = None
    locale: Optional[str] = None
    provider: Optional[str] = None
    model_id: Optional[str] = None


@dataclass
class AuditEvent:
    event_id: str
    timestamp: datetime
    user_id: str
    provider: str
    event_type: str
    metadata: Dict
    model_id: Optional[str] = None


@dataclass
class ModerationResult:
    is_approved: bool
    moderated_text: Optional[str] = None
    rejection_reasons: Optional[List[str]] = None
    model_id: Optional[str] = None


@dataclass
class ConsentTranslation:
    original_text: str
    translated_text: str
    target_language: str
    provider: str
    model_id: Optional[str] = None
