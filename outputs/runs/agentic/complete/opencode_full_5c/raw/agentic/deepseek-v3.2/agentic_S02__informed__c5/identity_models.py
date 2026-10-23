from typing import Dict, Any, Optional, List
from dataclasses import dataclass, asdict
from datetime import datetime
from enum import Enum


class LoginStatus(Enum):
    SUCCESS = "success"
    FAILED = "failed"
    PENDING = "pending"


class TokenType(Enum):
    ACCESS = "access_token"
    ID = "id_token"
    REFRESH = "refresh_token"


@dataclass
class AuthRequest:
    """Represents an authentication request."""

    provider: str
    redirect_uri: str
    state: str
    scope: str
    use_pkce: bool = False
    code_challenge: Optional[str] = None
    code_challenge_method: Optional[str] = None
    created_at: datetime = None

    def __post_init__(self):
        if self.created_at is None:
            self.created_at = datetime.utcnow()

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for serialization."""
        data = asdict(self)
        data["created_at"] = self.created_at.isoformat() if self.created_at else None
        return data


@dataclass
class TokenResponse:
    """Represents a token response from identity provider."""

    access_token: str
    token_type: str
    expires_in: int
    refresh_token: Optional[str] = None
    id_token: Optional[str] = None
    scope: Optional[str] = None
    provider: Optional[str] = None

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for serialization."""
        return asdict(self)

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "TokenResponse":
        """Create from dictionary."""
        return cls(**data)


@dataclass
class UserProfile:
    """Normalized user profile data."""

    provider: str
    user_id: str
    email: str
    email_verified: bool
    name: Optional[str] = None
    given_name: Optional[str] = None
    family_name: Optional[str] = None
    picture: Optional[str] = None
    locale: Optional[str] = None
    raw_profile: Optional[Dict[str, Any]] = None

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for serialization."""
        data = asdict(self)
        # Remove raw_profile if it's too large or sensitive
        if self.raw_profile:
            data["raw_profile"] = self.raw_profile
        return data

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "UserProfile":
        """Create from dictionary."""
        return cls(**data)


@dataclass
class LoginAuditRecord:
    """Audit record for login attempts."""

    id: str
    user_id: Optional[str]
    provider: str
    status: LoginStatus
    ip_address: Optional[str] = None
    user_agent: Optional[str] = None
    error_message: Optional[str] = None
    timestamp: datetime = None

    def __post_init__(self):
        if self.timestamp is None:
            self.timestamp = datetime.utcnow()

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for serialization."""
        data = asdict(self)
        data["status"] = self.status.value
        data["timestamp"] = self.timestamp.isoformat()
        return data

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "LoginAuditRecord":
        """Create from dictionary."""
        data["status"] = LoginStatus(data["status"])
        data["timestamp"] = datetime.fromisoformat(data["timestamp"])
        return cls(**data)


@dataclass
class ConsentTranslationRequest:
    """Request for consent text translation."""

    text: str
    source_language: str
    target_language: str
    context: Optional[str] = None

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for serialization."""
        return asdict(self)


@dataclass
class ClaimsModerationRequest:
    """Request for claims moderation."""

    text: str
    claim_type: str
    user_id: Optional[str] = None

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for serialization."""
        return asdict(self)


@dataclass
class ClaimsModerationResult:
    """Result of claims moderation."""

    is_approved: bool
    confidence: float
    reasons: List[str]
    moderated_text: Optional[str] = None

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for serialization."""
        return asdict(self)


def normalize_auth_response(
    response_data: Dict[str, Any], provider: str
) -> TokenResponse:
    """Normalize authentication response from different providers."""
    # Different providers may use different field names
    field_mapping = {
        "auth0": {
            "access_token": "access_token",
            "token_type": "token_type",
            "expires_in": "expires_in",
            "refresh_token": "refresh_token",
            "id_token": "id_token",
            "scope": "scope",
        },
        "cognito": {
            "access_token": "access_token",
            "token_type": "token_type",
            "expires_in": "expires_in",
            "refresh_token": "refresh_token",
            "id_token": "id_token",
            "scope": "scope",
        },
    }

    mapping = field_mapping.get(provider, field_mapping["auth0"])

    return TokenResponse(
        access_token=response_data.get(mapping["access_token"]),
        token_type=response_data.get(mapping["token_type"], "Bearer"),
        expires_in=response_data.get(mapping["expires_in"], 3600),
        refresh_token=response_data.get(mapping["refresh_token"]),
        id_token=response_data.get(mapping["id_token"]),
        scope=response_data.get(mapping["scope"]),
        provider=provider,
    )


def create_login_audit_record(
    user_id: Optional[str],
    provider: str,
    status: LoginStatus,
    ip_address: Optional[str] = None,
    user_agent: Optional[str] = None,
    error_message: Optional[str] = None,
) -> LoginAuditRecord:
    """Helper to create a login audit record."""
    import uuid

    return LoginAuditRecord(
        id=str(uuid.uuid4()),
        user_id=user_id,
        provider=provider,
        status=status,
        ip_address=ip_address,
        user_agent=user_agent,
        error_message=error_message,
    )
