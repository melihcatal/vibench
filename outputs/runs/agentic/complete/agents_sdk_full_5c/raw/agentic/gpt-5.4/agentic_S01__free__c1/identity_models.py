from __future__ import annotations

from dataclasses import dataclass, asdict
from typing import Any, Dict, Optional


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

    def to_identity_payload(self) -> Dict[str, Any]:
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
class IdentitySession:
    user_id: str
    email: str
    id_token: str
    refresh_token: str
    expires_in: int

    @classmethod
    def from_google_identity_toolkit(cls, payload: Dict[str, Any]) -> "IdentitySession":
        return cls(
            user_id=payload.get("localId", ""),
            email=payload.get("email", ""),
            id_token=payload["idToken"],
            refresh_token=payload["refreshToken"],
            expires_in=int(payload.get("expiresIn", 0)),
        )

    @classmethod
    def from_google_securetoken(cls, payload: Dict[str, Any], email: str = "") -> "IdentitySession":
        return cls(
            user_id=payload.get("user_id", ""),
            email=email,
            id_token=payload["id_token"],
            refresh_token=payload["refresh_token"],
            expires_in=int(payload.get("expires_in", 0)),
        )

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


@dataclass(slots=True)
class IdentityOperationResult:
    ok: bool
    provider: str
    detail: Dict[str, Any]

    def to_dict(self) -> Dict[str, Any]:
        return {
            "ok": self.ok,
            "provider": self.provider,
            "detail": self.detail,
        }


@dataclass(slots=True)
class TranslationResult:
    translated_text: str
    target_locale: str
    provider: str = "Google Cloud Translation"

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


@dataclass(slots=True)
class ModerationResult:
    allowed: bool
    flagged_categories: Dict[str, Any]
    provider: str = "OpenAI Moderations"

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


@dataclass(slots=True)
class SummaryResult:
    summary: str
    provider: str = "OpenAI Responses"

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


@dataclass(slots=True)
class DocumentStoreResult:
    document_id: str
    provider: str
    metadata: Dict[str, Any]

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


def compact_dict(data: Dict[str, Any]) -> Dict[str, Any]:
    return {k: v for k, v in data.items() if v is not None}
