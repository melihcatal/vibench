from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any, Mapping
from uuid import uuid4


def _utc_now() -> datetime:
    return datetime.now(timezone.utc)


def _as_str(value: Any) -> str:
    if value is None:
        return ""
    return str(value).strip()


def _first_non_empty(*values: Any) -> str:
    for value in values:
        text = _as_str(value)
        if text:
            return text
    return ""


def _normalize_identifier(value: Any) -> str:
    text = _as_str(value).lower()
    return text


def _to_mapping(value: Any) -> dict[str, Any]:
    if value is None:
        return {}
    if isinstance(value, Mapping):
        return dict(value)
    raise TypeError("Expected a mapping")


@dataclass(slots=True)
class FederatedLoginRequest:
    provider: str
    subject_token: str
    audience: str = ""
    scopes: list[str] = field(default_factory=list)
    claims: dict[str, Any] = field(default_factory=dict)
    nonce: str = ""
    requested_at: datetime = field(default_factory=_utc_now)

    @classmethod
    def from_dict(cls, payload: Mapping[str, Any]) -> "FederatedLoginRequest":
        data = _to_mapping(payload)
        scopes = data.get("scopes") or []
        if isinstance(scopes, str):
            scopes = [part for part in scopes.split() if part]
        return cls(
            provider=_normalize_identifier(data.get("provider")),
            subject_token=_as_str(data.get("subject_token") or data.get("token")),
            audience=_as_str(data.get("audience")),
            scopes=[_as_str(scope) for scope in scopes if _as_str(scope)],
            claims=_to_mapping(data.get("claims")),
            nonce=_as_str(data.get("nonce")) or uuid4().hex,
            requested_at=_parse_datetime(data.get("requested_at")) or _utc_now(),
        )


@dataclass(slots=True)
class FederatedLoginResponse:
    user_id: str
    provider: str
    provider_subject: str
    email: str = ""
    display_name: str = ""
    access_token: str = ""
    refresh_token: str = ""
    expires_at: datetime | None = None
    issued_at: datetime = field(default_factory=_utc_now)
    claims: dict[str, Any] = field(default_factory=dict)

    @property
    def is_expired(self) -> bool:
        return self.expires_at is not None and _utc_now() >= self.expires_at

    def to_dict(self) -> dict[str, Any]:
        return {
            "user_id": self.user_id,
            "provider": self.provider,
            "provider_subject": self.provider_subject,
            "email": self.email,
            "display_name": self.display_name,
            "access_token": self.access_token,
            "refresh_token": self.refresh_token,
            "expires_at": self.expires_at.isoformat() if self.expires_at else None,
            "issued_at": self.issued_at.isoformat(),
            "claims": dict(self.claims),
        }


def normalize_federated_login_claims(claims: Mapping[str, Any]) -> dict[str, Any]:
    data = _to_mapping(claims)
    provider = _normalize_identifier(data.get("provider") or data.get("iss") or data.get("issuer"))
    subject = _first_non_empty(data.get("sub"), data.get("subject"), data.get("id"))
    email = _first_non_empty(data.get("email"), data.get("preferred_username"), data.get("upn"))
    display_name = _first_non_empty(
        data.get("name"),
        data.get("display_name"),
        data.get("given_name"),
        data.get("preferred_username"),
    )
    expires_at = _parse_datetime(data.get("exp"))
    user_id = _first_non_empty(data.get("user_id"), f"{provider}:{subject}" if provider and subject else "", subject)
    return {
        "user_id": user_id,
        "provider": provider,
        "provider_subject": subject,
        "email": email,
        "display_name": display_name,
        "expires_at": expires_at,
        "claims": dict(data),
    }


def build_federated_login_response(claims: Mapping[str, Any], tokens: Mapping[str, Any] | None = None) -> FederatedLoginResponse:
    normalized = normalize_federated_login_claims(claims)
    token_data = _to_mapping(tokens)
    return FederatedLoginResponse(
        user_id=normalized["user_id"],
        provider=normalized["provider"],
        provider_subject=normalized["provider_subject"],
        email=normalized["email"],
        display_name=normalized["display_name"],
        access_token=_as_str(token_data.get("access_token")),
        refresh_token=_as_str(token_data.get("refresh_token")),
        expires_at=_parse_datetime(token_data.get("expires_at")) or normalized["expires_at"],
        claims=normalized["claims"],
    )


def _parse_datetime(value: Any) -> datetime | None:
    if value is None or value == "":
        return None
    if isinstance(value, datetime):
        return value.astimezone(timezone.utc) if value.tzinfo else value.replace(tzinfo=timezone.utc)
    if isinstance(value, (int, float)):
        return datetime.fromtimestamp(value, tz=timezone.utc)
    text = _as_str(value)
    try:
        if text.isdigit():
            return datetime.fromtimestamp(int(text), tz=timezone.utc)
        return datetime.fromisoformat(text.replace("Z", "+00:00")).astimezone(timezone.utc)
    except ValueError:
        return None
