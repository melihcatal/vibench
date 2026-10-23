# Federated Login Flow - Identity Models

from typing import Dict, Optional, List, TypedDict
from dataclasses import dataclass


class OAuthTokenResponse(TypedDict):
    access_token: str
    id_token: str
    refresh_token: Optional[str]
    expires_in: int
    token_type: str


class UserProfileClaims(TypedDict):
    sub: str
    name: Optional[str]
    given_name: Optional[str]
    family_name: Optional[str]
    email: Optional[str]
    email_verified: Optional[bool]
    picture: Optional[str]
    locale: Optional[str]
    updated_at: Optional[str]
    nickname: Optional[str]
    preferred_username: Optional[str]
    custom_claims: Optional[Dict[str, str]]


@dataclass
class AuditEvent:
    event_id: str
    timestamp: str
    user_id: str
    provider: str
    action: str
    metadata: Dict
    ip_address: Optional[str] = None
    user_agent: Optional[str] = None


@dataclass
class ModerationResult:
    is_flagged: bool
    flagged_categories: List[str]
    confidence_scores: Dict[str, float]
    suggested_action: str


@dataclass
class TranslationResult:
    translated_text: str
    detected_language: str
    provider: str
