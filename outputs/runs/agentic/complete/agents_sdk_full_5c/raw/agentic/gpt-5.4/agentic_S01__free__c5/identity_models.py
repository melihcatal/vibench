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
            "email": self.email.strip(),
            "password": self.password,
            "returnSecureToken": True,
        }
        if self.display_name:
            payload["displayName"] = self.display_name.strip()
        return payload


@dataclass(slots=True)
class LoginRequest:
    email: str
    password: str

    def to_identity_toolkit_payload(self) -> Dict[str, Any]:
        return {
            "email": self.email.strip(),
            "password": self.password,
            "returnSecureToken": True,
        }


@dataclass(slots=True)
class RefreshSessionRequest:
    refresh_token: str

    def to_refresh_payload(self) -> Dict[str, Any]:
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
            "email": self.email.strip(),
        }


@dataclass(slots=True)
class AccountTokens:
    id_token: str
    refresh_token: str
    expires_in: int


@dataclass(slots=True)
class IdentityUser:
    local_id: str
    email: str
    display_name: Optional[str] = None


@dataclass(slots=True)
class IdentityResult:
    user: IdentityUser
    tokens: Optional[AccountTokens] = None
    raw: Dict[str, Any] = field(default_factory=dict)


@dataclass(slots=True)
class TranslationResult:
    translated_text: str
    detected_language: Optional[str]
    raw: Dict[str, Any] = field(default_factory=dict)


@dataclass(slots=True)
class ModerationResult:
    flagged: bool
    categories: List[str]
    raw: Dict[str, Any] = field(default_factory=dict)


@dataclass(slots=True)
class SummaryResult:
    summary: str
    raw: Dict[str, Any] = field(default_factory=dict)


@dataclass(slots=True)
class StoredNoteResult:
    document_path: str
    update_time: Optional[str]
    raw: Dict[str, Any] = field(default_factory=dict)


def normalize_identity_result(payload: Dict[str, Any]) -> IdentityResult:
    user = IdentityUser(
        local_id=payload.get("localId", ""),
        email=payload.get("email", ""),
        display_name=payload.get("displayName"),
    )
    tokens = None
    if payload.get("idToken") and payload.get("refreshToken"):
        tokens = AccountTokens(
            id_token=payload["idToken"],
            refresh_token=payload["refreshToken"],
            expires_in=int(payload.get("expiresIn", 0) or 0),
        )
    return IdentityResult(user=user, tokens=tokens, raw=payload)


def normalize_refresh_result(payload: Dict[str, Any]) -> AccountTokens:
    return AccountTokens(
        id_token=payload["id_token"],
        refresh_token=payload["refresh_token"],
        expires_in=int(payload.get("expires_in", 0) or 0),
    )


def compact_categories(result: Dict[str, Any]) -> List[str]:
    categories: List[str] = []
    category_scores = result.get("categories", {})
    for name, enabled in category_scores.items():
        if enabled:
            categories.append(name)
    return categories
