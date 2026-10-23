from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional


@dataclass(slots=True)
class RegisterUserRequest:
    email: str
    password: str
    display_name: Optional[str] = None

    def to_identity_payload(self) -> Dict[str, Any]:
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

    def to_identity_payload(self) -> Dict[str, Any]:
        return {
            "email": self.email,
            "password": self.password,
            "returnSecureToken": True,
        }


@dataclass(slots=True)
class RefreshSessionRequest:
    refresh_token: str

    def to_identity_payload(self) -> Dict[str, str]:
        return {
            "grant_type": "refresh_token",
            "refresh_token": self.refresh_token,
        }


@dataclass(slots=True)
class PasswordResetRequest:
    email: str

    def to_identity_payload(self) -> Dict[str, Any]:
        return {
            "requestType": "PASSWORD_RESET",
            "email": self.email,
        }


@dataclass(slots=True)
class AuthTokens:
    access_token: str
    refresh_token: str
    expires_in: int
    id_token: Optional[str] = None
    token_type: str = "Bearer"


@dataclass(slots=True)
class UserAccount:
    user_id: str
    email: str
    display_name: Optional[str] = None
    id_token: Optional[str] = None
    refresh_token: Optional[str] = None
    expires_in: Optional[int] = None


@dataclass(slots=True)
class TranslationResult:
    translated_text: str
    target_locale: str
    provider: str = "deepl"


@dataclass(slots=True)
class ModerationResult:
    approved: bool
    provider: str
    risk_scores: Dict[str, float] = field(default_factory=dict)
    flagged_categories: List[str] = field(default_factory=list)
    raw_response: Dict[str, Any] = field(default_factory=dict)


@dataclass(slots=True)
class OnboardingSummary:
    summary: str
    provider: str
    model: str


@dataclass(slots=True)
class ProfileNoteRecord:
    note_id: str
    user_id: str
    provider: str
    stored: bool
    document: Dict[str, Any]


def normalize_firebase_auth_response(payload: Dict[str, Any]) -> AuthTokens:
    return AuthTokens(
        access_token=payload.get("idToken", ""),
        refresh_token=payload.get("refreshToken", ""),
        expires_in=int(payload.get("expiresIn", 0)),
        id_token=payload.get("idToken"),
        token_type="Bearer",
    )


def normalize_firebase_user_response(payload: Dict[str, Any]) -> UserAccount:
    return UserAccount(
        user_id=payload.get("localId", ""),
        email=payload.get("email", ""),
        display_name=payload.get("displayName"),
        id_token=payload.get("idToken"),
        refresh_token=payload.get("refreshToken"),
        expires_in=int(payload.get("expiresIn", 0)) if payload.get("expiresIn") else None,
    )
