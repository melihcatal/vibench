from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Mapping, Optional
from uuid import uuid4


def _string_or_none(value: Any) -> Optional[str]:
    if value is None:
        return None
    if isinstance(value, str):
        value = value.strip()
        return value or None
    return str(value)


def _bool(value: Any) -> bool:
    if isinstance(value, bool):
        return value
    if value is None:
        return False
    if isinstance(value, (int, float)):
        return value != 0
    if isinstance(value, str):
        return value.strip().lower() in {"1", "true", "yes", "y", "on"}
    return bool(value)


def normalize_provider_name(value: Any) -> Optional[str]:
    name = _string_or_none(value)
    if name is None:
        return None
    return name.lower().replace(" ", "_")


def normalize_email(value: Any) -> Optional[str]:
    email = _string_or_none(value)
    if email is None:
        return None
    return email.lower()


def normalize_identity_id(value: Any) -> str:
    identity_id = _string_or_none(value)
    return identity_id if identity_id is not None else uuid4().hex


@dataclass(frozen=True)
class FederatedLoginRequest:
    provider: str
    token: str
    email: Optional[str] = None
    state: Optional[str] = None
    redirect_uri: Optional[str] = None
    audience: Optional[str] = None
    scopes: tuple[str, ...] = field(default_factory=tuple)

    @classmethod
    def from_mapping(cls, data: Mapping[str, Any]) -> "FederatedLoginRequest":
        scopes = data.get("scopes") or ()
        if isinstance(scopes, str):
            scopes = tuple(part for part in scopes.split() if part)
        else:
            scopes = tuple(_string_or_none(item) for item in scopes)
            scopes = tuple(item for item in scopes if item)
        return cls(
            provider=normalize_provider_name(data.get("provider")) or "",
            token=_string_or_none(data.get("token")) or "",
            email=normalize_email(data.get("email")),
            state=_string_or_none(data.get("state")),
            redirect_uri=_string_or_none(data.get("redirect_uri")),
            audience=_string_or_none(data.get("audience")),
            scopes=scopes,
        )

    def normalized(self) -> "FederatedLoginRequest":
        return FederatedLoginRequest(
            provider=normalize_provider_name(self.provider) or "",
            token=_string_or_none(self.token) or "",
            email=normalize_email(self.email),
            state=_string_or_none(self.state),
            redirect_uri=_string_or_none(self.redirect_uri),
            audience=_string_or_none(self.audience),
            scopes=tuple(_string_or_none(scope) for scope in self.scopes if _string_or_none(scope)),
        )


@dataclass(frozen=True)
class FederatedLoginResponse:
    success: bool
    identity_id: str
    provider: str
    email: Optional[str] = None
    access_token: Optional[str] = None
    refresh_token: Optional[str] = None
    expires_in: Optional[int] = None
    id_token: Optional[str] = None
    error: Optional[str] = None
    raw: Optional[Mapping[str, Any]] = None

    @classmethod
    def from_mapping(cls, data: Mapping[str, Any]) -> "FederatedLoginResponse":
        expires_in = data.get("expires_in")
        if expires_in is not None:
            try:
                expires_in = int(expires_in)
            except (TypeError, ValueError):
                expires_in = None
        return cls(
            success=_bool(data.get("success", True)),
            identity_id=normalize_identity_id(data.get("identity_id")),
            provider=normalize_provider_name(data.get("provider")) or "",
            email=normalize_email(data.get("email")),
            access_token=_string_or_none(data.get("access_token")),
            refresh_token=_string_or_none(data.get("refresh_token")),
            expires_in=expires_in,
            id_token=_string_or_none(data.get("id_token")),
            error=_string_or_none(data.get("error")),
            raw=data,
        )

    def normalized(self) -> "FederatedLoginResponse":
        return FederatedLoginResponse(
            success=_bool(self.success),
            identity_id=normalize_identity_id(self.identity_id),
            provider=normalize_provider_name(self.provider) or "",
            email=normalize_email(self.email),
            access_token=_string_or_none(self.access_token),
            refresh_token=_string_or_none(self.refresh_token),
            expires_in=int(self.expires_in) if self.expires_in is not None else None,
            id_token=_string_or_none(self.id_token),
            error=_string_or_none(self.error),
            raw=self.raw,
        )


@dataclass(frozen=True)
class FederatedIdentity:
    identity_id: str
    provider: str
    subject: Optional[str] = None
    email: Optional[str] = None
    display_name: Optional[str] = None
    given_name: Optional[str] = None
    family_name: Optional[str] = None
    picture_url: Optional[str] = None
    locale: Optional[str] = None
    verified_email: bool = False
    metadata: dict[str, Any] = field(default_factory=dict)

    @classmethod
    def from_mapping(cls, data: Mapping[str, Any]) -> "FederatedIdentity":
        return cls(
            identity_id=normalize_identity_id(data.get("identity_id")),
            provider=normalize_provider_name(data.get("provider")) or "",
            subject=_string_or_none(data.get("subject")),
            email=normalize_email(data.get("email")),
            display_name=_string_or_none(data.get("display_name")),
            given_name=_string_or_none(data.get("given_name")),
            family_name=_string_or_none(data.get("family_name")),
            picture_url=_string_or_none(data.get("picture_url")),
            locale=_string_or_none(data.get("locale")),
            verified_email=_bool(data.get("verified_email")),
            metadata=dict(data.get("metadata") or {}),
        )

    def normalized(self) -> "FederatedIdentity":
        return FederatedIdentity(
            identity_id=normalize_identity_id(self.identity_id),
            provider=normalize_provider_name(self.provider) or "",
            subject=_string_or_none(self.subject),
            email=normalize_email(self.email),
            display_name=_string_or_none(self.display_name),
            given_name=_string_or_none(self.given_name),
            family_name=_string_or_none(self.family_name),
            picture_url=_string_or_none(self.picture_url),
            locale=_string_or_none(self.locale),
            verified_email=_bool(self.verified_email),
            metadata=dict(self.metadata),
        )
