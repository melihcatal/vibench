from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


@dataclass(frozen=True)
class RegisterUserRequest:
    email: str
    password: str
    display_name: str | None = None
    locale: str | None = None
    metadata: dict[str, Any] = field(default_factory=dict)

    def to_payload(self) -> dict[str, Any]:
        metadata = dict(self.metadata)
        if self.display_name is not None:
            metadata["display_name"] = self.display_name
        if self.locale is not None:
            metadata["locale"] = self.locale
        return {"email": self.email.strip().lower(), "password": self.password, "metadata": metadata}


@dataclass(frozen=True)
class LoginRequest:
    email: str
    password: str

    def to_payload(self) -> dict[str, str]:
        return {"email": self.email.strip().lower(), "password": self.password}


@dataclass(frozen=True)
class RefreshSessionRequest:
    refresh_token: str

    def to_payload(self) -> dict[str, str]:
        return {"refresh_token": self.refresh_token}


@dataclass(frozen=True)
class PasswordResetRequest:
    email: str
    redirect_to: str | None = None

    def to_payload(self) -> dict[str, Any]:
        options: dict[str, Any] = {}
        if self.redirect_to:
            options["redirect_to"] = self.redirect_to
        return {"email": self.email.strip().lower(), "options": options}


def _record_to_dict(record: Any) -> dict[str, Any]:
    if record is None:
        return {}
    if isinstance(record, dict):
        return dict(record)
    if hasattr(record, "model_dump"):
        return record.model_dump()
    if hasattr(record, "__dict__"):
        return dict(record.__dict__)
    return {"value": record}


def normalize_user_record(user: Any, provider: str) -> dict[str, Any]:
    data = _record_to_dict(user)
    return {"provider": provider, "user": data}


def normalize_session_record(session_result: Any, provider: str) -> dict[str, Any]:
    data = _record_to_dict(getattr(session_result, "session", None) or session_result)
    user = _record_to_dict(getattr(session_result, "user", None) or data.get("user"))
    return {"provider": provider, "session": data, "user": user}


def normalize_operation_status(result: Any, provider: str) -> dict[str, Any]:
    return {"provider": provider, "status": "ok", "result": _record_to_dict(result)}
