from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, Mapping, Optional


@dataclass(slots=True)
class RegistrationRequest:
    email: str
    password: str
    given_name: Optional[str] = None
    family_name: Optional[str] = None
    user_metadata: Dict[str, Any] = field(default_factory=dict)

    def to_auth0_payload(self, connection: str) -> Dict[str, Any]:
        payload: Dict[str, Any] = {
            "client_id": None,
            "email": self.email.strip().lower(),
            "password": self.password,
            "connection": connection,
        }
        if self.given_name or self.family_name:
            payload["user_metadata"] = {
                **self.user_metadata,
                "given_name": self.given_name,
                "family_name": self.family_name,
            }
        elif self.user_metadata:
            payload["user_metadata"] = dict(self.user_metadata)
        return payload


@dataclass(slots=True)
class LoginRequest:
    email: str
    password: str
    audience: Optional[str] = None
    scope: str = "openid profile email offline_access"


@dataclass(slots=True)
class TokenResponse:
    access_token: str
    expires_in: int
    token_type: str
    refresh_token: Optional[str] = None
    id_token: Optional[str] = None
    scope: Optional[str] = None

    @classmethod
    def from_mapping(cls, data: Mapping[str, Any]) -> "TokenResponse":
        return cls(
            access_token=str(data.get("access_token", "")),
            expires_in=int(data.get("expires_in", 0)),
            token_type=str(data.get("token_type", "")),
            refresh_token=data.get("refresh_token"),
            id_token=data.get("id_token"),
            scope=data.get("scope"),
        )


@dataclass(slots=True)
class PasswordResetRequest:
    email: str


@dataclass(slots=True)
class TranslationResult:
    source_text: str
    translated_text: str
    target_locale: str
    provider: str = "deepl"


@dataclass(slots=True)
class ModerationResult:
    allowed: bool
    provider: str
    flagged: bool
    scores: Dict[str, float] = field(default_factory=dict)
    normalized_text: str = ""


@dataclass(slots=True)
class SummaryResult:
    summary: str
    model: str
    provider: str = "openai"


@dataclass(slots=True)
class DocumentWriteResult:
    document_id: str
    etag: Optional[str]
    provider: str = "azure_cosmos_db"


def normalize_email(value: str) -> str:
    return value.strip().lower()


def compact_dict(data: Mapping[str, Any]) -> Dict[str, Any]:
    return {k: v for k, v in data.items() if v is not None}
