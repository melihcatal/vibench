from dataclasses import dataclass, field
from typing import Optional, Dict, Any, List


@dataclass
class UserProfile:
    sub: str
    name: Optional[str] = None
    given_name: Optional[str] = None
    family_name: Optional[str] = None
    nickname: Optional[str] = None
    preferred_username: Optional[str] = None
    profile: Optional[str] = None
    picture: Optional[str] = None
    website: Optional[str] = None
    email: Optional[str] = None
    email_verified: Optional[bool] = None
    gender: Optional[str] = None
    birthdate: Optional[str] = None
    zoneinfo: Optional[str] = None
    locale: Optional[str] = None
    phone_number: Optional[str] = None
    phone_number_verified: Optional[bool] = None
    address: Optional[Dict[str, Any]] = None
    updated_at: Optional[str] = None
    # Custom claims
    custom_claims: Dict[str, Any] = field(default_factory=dict)


@dataclass
class TokenResponse:
    access_token: str
    id_token: Optional[str] = None
    refresh_token: Optional[str] = None
    expires_in: Optional[int] = None
    token_type: Optional[str] = None


@dataclass
class OAuthCallbackRequest:
    code: str
    state: Optional[str] = None
    redirect_uri: Optional[str] = None
    code_verifier: Optional[str] = None


@dataclass
class AuditRecord:
    timestamp: str
    event_type: str
    user_id: str
    ip_address: str
    user_agent: str
    details: Dict[str, Any]
