from dataclasses import dataclass, field
from typing import Optional, Dict, Any, List
from datetime import datetime


@dataclass
class UserProfile:
    """User profile data from identity provider."""

    sub: str
    email: Optional[str] = None
    email_verified: bool = False
    name: Optional[str] = None
    given_name: Optional[str] = None
    family_name: Optional[str] = None
    picture: Optional[str] = None
    locale: Optional[str] = None
    provider: str = "unknown"
    raw_claims: Dict[str, Any] = field(default_factory=dict)


@dataclass
class NormalizedProfile:
    """Normalized user profile with standard fields."""

    user_id: str
    email: Optional[str] = None
    email_verified: bool = False
    full_name: Optional[str] = None
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    avatar_url: Optional[str] = None
    locale: Optional[str] = None
    provider: str = "unknown"
    original_profile: Optional[UserProfile] = None
    normalized_at: datetime = field(default_factory=datetime.now)


@dataclass
class TokenResponse:
    """OAuth token response."""

    access_token: str
    refresh_token: Optional[str] = None
    id_token: Optional[str] = None
    expires_in: int = 3600
    token_type: str = "Bearer"
    user_info: Optional[UserProfile] = None
    received_at: datetime = field(default_factory=datetime.now)


@dataclass
class AuthRequest:
    """Authentication request data."""

    provider: str
    state: str
    nonce: Optional[str] = None
    code_verifier: Optional[str] = None
    redirect_uri: Optional[str] = None
    scopes: List[str] = field(default_factory=list)
    created_at: datetime = field(default_factory=datetime.now)


@dataclass
class AuthResponse:
    """Authentication response data."""

    success: bool
    user_profile: Optional[NormalizedProfile] = None
    tokens: Optional[TokenResponse] = None
    error: Optional[str] = None
    error_description: Optional[str] = None
    completed_at: datetime = field(default_factory=datetime.now)


@dataclass
class ConsentData:
    """Consent screen data."""

    provider: str
    scopes: List[str]
    client_name: str
    privacy_policy_url: Optional[str] = None
    terms_of_service_url: Optional[str] = None
    logo_url: Optional[str] = None


@dataclass
class AuditEvent:
    """Audit event for federated login."""

    event_id: str
    event_type: str
    user_id: Optional[str] = None
    provider: Optional[str] = None
    ip_address: Optional[str] = None
    user_agent: Optional[str] = None
    success: bool = True
    error_message: Optional[str] = None
    metadata: Dict[str, Any] = field(default_factory=dict)
    timestamp: datetime = field(default_factory=datetime.now)


def create_user_profile_from_claims(
    claims: Dict[str, Any], provider: str
) -> UserProfile:
    """Create UserProfile from raw claims dictionary."""
    return UserProfile(
        sub=claims.get("sub") or claims.get("user_id") or str(claims.get("id", "")),
        email=claims.get("email")
        or claims.get("mail")
        or claims.get("preferred_username"),
        email_verified=claims.get("email_verified", False)
        or claims.get("verified", False),
        name=claims.get("name") or claims.get("display_name"),
        given_name=claims.get("given_name") or claims.get("first_name"),
        family_name=claims.get("family_name")
        or claims.get("last_name")
        or claims.get("surname"),
        picture=claims.get("picture")
        or claims.get("avatar_url")
        or claims.get("photo_url"),
        locale=claims.get("locale") or claims.get("language"),
        provider=provider,
        raw_claims=claims,
    )


def normalize_profile_fields(profile: UserProfile) -> NormalizedProfile:
    """Normalize profile fields to standard format."""
    return NormalizedProfile(
        user_id=profile.sub,
        email=profile.email,
        email_verified=profile.email_verified,
        full_name=profile.name,
        first_name=profile.given_name,
        last_name=profile.family_name,
        avatar_url=profile.picture,
        locale=profile.locale,
        provider=profile.provider,
        original_profile=profile,
    )
