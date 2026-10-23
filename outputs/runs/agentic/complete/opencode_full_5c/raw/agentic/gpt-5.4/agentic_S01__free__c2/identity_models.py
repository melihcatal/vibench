from __future__ import annotations

from dataclasses import asdict, dataclass, field
from typing import Any, Dict, List, Optional


def _clean_dict(values: Dict[str, Any]) -> Dict[str, Any]:
    return {key: value for key, value in values.items() if value is not None}


@dataclass
class RegisterUserRequest:
    email: str
    password: str
    connection: str = "Username-Password-Authentication"
    user_metadata: Dict[str, Any] = field(default_factory=dict)

    def to_auth0_payload(self) -> Dict[str, Any]:
        payload = {
            "email": self.email,
            "password": self.password,
            "connection": self.connection,
        }
        if self.user_metadata:
            payload["user_metadata"] = self.user_metadata
        return payload


@dataclass
class LoginRequest:
    email: str
    password: str
    audience: Optional[str] = None
    scope: str = "openid profile email offline_access"
    realm: str = "Username-Password-Authentication"


@dataclass
class RefreshSessionRequest:
    refresh_token: str
    scope: Optional[str] = None


@dataclass
class PasswordResetRequest:
    email: str
    connection: str = "Username-Password-Authentication"


@dataclass
class TokenResponse:
    access_token: str
    expires_in: int
    token_type: str
    refresh_token: Optional[str] = None
    id_token: Optional[str] = None
    scope: Optional[str] = None

    @classmethod
    def from_auth0(cls, payload: Dict[str, Any]) -> "TokenResponse":
        return cls(
            access_token=payload["access_token"],
            expires_in=payload["expires_in"],
            token_type=payload["token_type"],
            refresh_token=payload.get("refresh_token"),
            id_token=payload.get("id_token"),
            scope=payload.get("scope"),
        )

    def to_dict(self) -> Dict[str, Any]:
        return _clean_dict(asdict(self))


@dataclass
class UserAccountResponse:
    user_id: str
    email: str
    email_verified: bool
    created_at: Optional[str] = None
    updated_at: Optional[str] = None
    identities: List[Dict[str, Any]] = field(default_factory=list)
    user_metadata: Dict[str, Any] = field(default_factory=dict)
    app_metadata: Dict[str, Any] = field(default_factory=dict)

    @classmethod
    def from_auth0(cls, payload: Dict[str, Any]) -> "UserAccountResponse":
        return cls(
            user_id=payload["user_id"],
            email=payload["email"],
            email_verified=payload.get("email_verified", False),
            created_at=payload.get("created_at"),
            updated_at=payload.get("updated_at"),
            identities=payload.get("identities", []),
            user_metadata=payload.get("user_metadata", {}),
            app_metadata=payload.get("app_metadata", {}),
        )

    def to_dict(self) -> Dict[str, Any]:
        return _clean_dict(asdict(self))


@dataclass
class PasswordResetResponse:
    email: str
    status: str

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


@dataclass
class TranslationResult:
    locale: str
    translated_text: str
    model: str

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


@dataclass
class ModerationResult:
    approved: bool
    flagged: bool
    categories: Dict[str, bool]
    category_scores: Dict[str, float]
    model: str

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


@dataclass
class OnboardingSummary:
    summary: str
    model: str

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


@dataclass
class StoredProfileNote:
    table_name: str
    note_id: str
    stored: bool

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)
