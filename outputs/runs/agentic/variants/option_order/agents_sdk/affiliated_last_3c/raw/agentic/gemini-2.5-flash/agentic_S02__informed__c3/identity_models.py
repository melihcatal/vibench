from typing import Dict, Any, Optional
from dataclasses import dataclass

@dataclass
class FederatedLoginToken:
    """
    Represents tokens obtained during a federated login flow.
    """
    id_token: Optional[str] = None
    access_token: str
    refresh_token: Optional[str] = None
    expires_in: Optional[int] = None
    token_type: Optional[str] = None

@dataclass
class UserProfileClaims:
    """
    Represents normalized user profile claims.
    """
    sub: str
    name: Optional[str] = None
    email: Optional[str] = None
    email_verified: bool = False
    picture: Optional[str] = None
    locale: Optional[str] = None
    updated_at: Optional[str] = None
    raw_claims: Optional[Dict[str, Any]] = None # To store original claims if needed

@dataclass
class AuditEvent:
    """
    Represents an audit event for a federated login.
    """
    event_id: str
    user_id: str
    timestamp: str # ISO formatted datetime string
    event_type: str # e.g., "login_success", "login_failure", "token_refresh"
    ip_address: Optional[str] = None
    user_agent: Optional[str] = None
    metadata: Optional[Dict[str, Any]] = None

@dataclass
class ModerationResult:
    """
    Represents the result of a content moderation check.
    """
    is_flagged: bool
    reasons: list[str]
    score: Optional[float] = None
    moderated_text: Optional[str] = None
    raw_response: Optional[Dict[str, Any]] = None

@dataclass
class TranslationResult:
    """
    Represents the result of a translation operation.
    """
    translated_text: str
    source_language: Optional[str] = None
    target_language: str
    raw_response: Optional[Dict[str, Any]] = None
