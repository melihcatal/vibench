from dataclasses import dataclass, field
from typing import Any, Dict, Optional, Tuple


@dataclass(frozen=True)
class TokenPair:
    access_token: Optional[str] = None
    id_token: Optional[str] = None
    refresh_token: Optional[str] = None
    token_type: Optional[str] = None
    expires_in: Optional[int] = None


@dataclass(frozen=True)
class UserRecord:
    user_id: Optional[str] = None
    email: Optional[str] = None
    email_verified: Optional[bool] = None
    name: Optional[str] = None
    locale: Optional[str] = None
    raw: Dict[str, Any] = field(default_factory=dict)


@dataclass(frozen=True)
class RegisterUserRequest:
    email: str
    password: str
    locale: Optional[str] = None
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass(frozen=True)
class LoginRequest:
    email: str
    password: str
    locale: Optional[str] = None


@dataclass(frozen=True)
class RefreshRequest:
    refresh_token: str
    scope: Optional[str] = None


@dataclass(frozen=True)
class PasswordResetRequest:
    email: str
    locale: Optional[str] = None


@dataclass(frozen=True)
class RegisterUserResponse:
    user: UserRecord
    tokens: TokenPair


@dataclass(frozen=True)
class LoginResponse:
    user: UserRecord
    tokens: TokenPair


@dataclass(frozen=True)
class RefreshResponse:
    tokens: TokenPair


@dataclass(frozen=True)
class PasswordResetResponse:
    message: str



def normalize_user_record(data: Dict[str, Any]) -> UserRecord:
    return UserRecord(
        user_id=data.get("user_id") or data.get("sub") or data.get("id"),
        email=data.get("email"),
        email_verified=data.get("email_verified"),
        name=data.get("name") or data.get("nickname") or data.get("given_name"),
        locale=data.get("locale"),
        raw=data,
    )



def extract_token_pair(data: Dict[str, Any]) -> TokenPair:
    return TokenPair(
        access_token=data.get("access_token"),
        id_token=data.get("id_token"),
        refresh_token=data.get("refresh_token"),
        token_type=data.get("token_type"),
        expires_in=data.get("expires_in"),
    )
