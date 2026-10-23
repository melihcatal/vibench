from dataclasses import dataclass, field
from typing import Optional, List, Dict, Any


@dataclass
class AuthTokens:
    access_token: str
    refresh_token: Optional[str] = None
    id_token: Optional[str] = None
    expires_in: Optional[int] = None
    token_type: Optional[str] = None


@dataclass
class UserProfile:
    user_id: str
    email: str
    attributes: Dict[str, Any] = field(default_factory=dict)


@dataclass
class TranslatedContent:
    original_text: str
    translated_text: str
    target_language: str


@dataclass
class ModerationResult:
    text: str
    is_safe: bool
    reasons: List[str] = field(default_factory=list)


@dataclass
class OnboardingSummary:
    user_id: str
    summary_text: str
    status: str


@dataclass
class ProfileNote:
    user_id: str
    note_id: str
    content: str
    timestamp: str
    metadata: Dict[str, Any] = field(default_factory=dict)
