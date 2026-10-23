from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional


@dataclass(slots=True)
class RegisterUserRequest:
    email: str
    password: str
    display_name: Optional[str] = None

    def to_identity_toolkit_payload(self) -> Dict[str, Any]:
        payload: Dict[str, Any] = {
            "email": self.email,
            "password": self.password,
            "returnSecureToken": True,
        }
        if self.display_name:
            payload["displayName"] = self.display_name
        return payload


@dataclass(slots=True)
class LoginRequest:
    email: str
    password: str

    def to_identity_toolkit_payload(self) -> Dict[str, Any]:
        return {
            "email": self.email,
            "password": self.password,
            "returnSecureToken": True,
        }


@dataclass(slots=True)
class RefreshSessionRequest:
    refresh_token: str

    def to_securetoken_payload(self) -> Dict[str, Any]:
        return {
            "grant_type": "refresh_token",
            "refresh_token": self.refresh_token,
        }


@dataclass(slots=True)
class PasswordResetRequest:
    email: str

    def to_identity_toolkit_payload(self) -> Dict[str, Any]:
        return {
            "requestType": "PASSWORD_RESET",
            "email": self.email,
        }


@dataclass(slots=True)
class AuthTokens:
    id_token: Optional[str] = None
    refresh_token: Optional[str] = None
    access_token: Optional[str] = None
    expires_in: Optional[int] = None
    token_type: str = "Bearer"


@dataclass(slots=True)
class UserAccount:
    email: str
    local_id: Optional[str] = None
    display_name: Optional[str] = None
    email_verified: Optional[bool] = None
    tokens: AuthTokens = field(default_factory=AuthTokens)


@dataclass(slots=True)
class TranslationResult:
    translated_text: str
    detected_language: Optional[str] = None
    target_language: Optional[str] = None
    provider: str = "google_translate_v2"


@dataclass(slots=True)
class ModerationResult:
    allowed: bool
    flagged_categories: List[str]
    score_map: Dict[str, float]
    provider: str = "openai_moderation"


@dataclass(slots=True)
class SummaryResult:
    summary: str
    provider: str = "openai_chat"


@dataclass(slots=True)
class DocumentStoreResult:
    document_id: str
    provider: str = "google_firestore"



def parse_auth_response(data: Dict[str, Any]) -> UserAccount:
    expires_raw = data.get("expiresIn")
    expires_in = int(expires_raw) if expires_raw is not None else None
    tokens = AuthTokens(
        id_token=data.get("idToken"),
        refresh_token=data.get("refreshToken"),
        access_token=data.get("access_token"),
        expires_in=expires_in,
    )
    return UserAccount(
        email=data.get("email", ""),
        local_id=data.get("localId") or data.get("user_id"),
        display_name=data.get("displayName"),
        email_verified=data.get("registered") or data.get("emailVerified"),
        tokens=tokens,
    )



def parse_refresh_response(data: Dict[str, Any]) -> AuthTokens:
    expires_raw = data.get("expires_in")
    expires_in = int(expires_raw) if expires_raw is not None else None
    return AuthTokens(
        id_token=data.get("id_token"),
        refresh_token=data.get("refresh_token"),
        access_token=data.get("access_token"),
        expires_in=expires_in,
        token_type=data.get("token_type", "Bearer"),
    )
