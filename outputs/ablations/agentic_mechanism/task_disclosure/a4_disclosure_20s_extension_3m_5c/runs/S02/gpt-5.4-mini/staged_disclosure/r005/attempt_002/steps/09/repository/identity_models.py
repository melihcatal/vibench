from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Mapping, Optional


def _coerce_str(value: Any) -> Optional[str]:
    if value is None:
        return None
    text = str(value).strip()
    return text or None


def _coerce_bool(value: Any) -> Optional[bool]:
    if value is None:
        return None
    if isinstance(value, bool):
        return value
    if isinstance(value, (int, float)):
        return bool(value)
    text = str(value).strip().lower()
    if text in {"1", "true", "yes", "y", "on"}:
        return True
    if text in {"0", "false", "no", "n", "off"}:
        return False
    return None


def _normalize_email(value: Any) -> Optional[str]:
    email = _coerce_str(value)
    return email.lower() if email else None


def _normalize_provider(value: Any) -> Optional[str]:
    provider = _coerce_str(value)
    return provider.lower().replace(" ", "_") if provider else None


@dataclass(slots=True)
class FederatedLoginRequest:
    provider: str
    token: Optional[str] = None
    code: Optional[str] = None
    redirect_uri: Optional[str] = None
    state: Optional[str] = None
    nonce: Optional[str] = None
    scope: Optional[str] = None
    email: Optional[str] = None
    metadata: dict[str, Any] = field(default_factory=dict)

    @classmethod
    def from_mapping(cls, data: Mapping[str, Any]) -> "FederatedLoginRequest":
        return cls(
            provider=_normalize_provider(data.get("provider")) or "",
            token=_coerce_str(data.get("token")),
            code=_coerce_str(data.get("code")),
            redirect_uri=_coerce_str(data.get("redirect_uri")),
            state=_coerce_str(data.get("state")),
            nonce=_coerce_str(data.get("nonce")),
            scope=_coerce_str(data.get("scope")),
            email=_normalize_email(data.get("email")),
            metadata=dict(data.get("metadata") or {}),
        )

    def normalize(self) -> "FederatedLoginRequest":
        return FederatedLoginRequest(
            provider=_normalize_provider(self.provider) or self.provider,
            token=_coerce_str(self.token),
            code=_coerce_str(self.code),
            redirect_uri=_coerce_str(self.redirect_uri),
            state=_coerce_str(self.state),
            nonce=_coerce_str(self.nonce),
            scope=_coerce_str(self.scope),
            email=_normalize_email(self.email),
            metadata=dict(self.metadata),
        )


@dataclass(slots=True)
class FederatedLoginResponse:
    success: bool
    subject: Optional[str] = None
    provider: Optional[str] = None
    email: Optional[str] = None
    access_token: Optional[str] = None
    refresh_token: Optional[str] = None
    expires_in: Optional[int] = None
    id_token: Optional[str] = None
    error: Optional[str] = None
    error_description: Optional[str] = None
    raw: dict[str, Any] = field(default_factory=dict)

    @classmethod
    def from_mapping(cls, data: Mapping[str, Any]) -> "FederatedLoginResponse":
        return cls(
            success=bool(data.get("success", False)),
            subject=_coerce_str(data.get("subject")),
            provider=_normalize_provider(data.get("provider")),
            email=_normalize_email(data.get("email")),
            access_token=_coerce_str(data.get("access_token")),
            refresh_token=_coerce_str(data.get("refresh_token")),
            expires_in=int(data["expires_in"]) if data.get("expires_in") is not None else None,
            id_token=_coerce_str(data.get("id_token")),
            error=_coerce_str(data.get("error")),
            error_description=_coerce_str(data.get("error_description")),
            raw=dict(data),
        )

    def normalize(self) -> "FederatedLoginResponse":
        return FederatedLoginResponse(
            success=bool(self.success),
            subject=_coerce_str(self.subject),
            provider=_normalize_provider(self.provider),
            email=_normalize_email(self.email),
            access_token=_coerce_str(self.access_token),
            refresh_token=_coerce_str(self.refresh_token),
            expires_in=int(self.expires_in) if self.expires_in is not None else None,
            id_token=_coerce_str(self.id_token),
            error=_coerce_str(self.error),
            error_description=_coerce_str(self.error_description),
            raw=dict(self.raw),
        )


def normalize_federated_login_request(data: Mapping[str, Any] | FederatedLoginRequest) -> FederatedLoginRequest:
    return data.normalize() if isinstance(data, FederatedLoginRequest) else FederatedLoginRequest.from_mapping(data).normalize()


def normalize_federated_login_response(data: Mapping[str, Any] | FederatedLoginResponse) -> FederatedLoginResponse:
    return data.normalize() if isinstance(data, FederatedLoginResponse) else FederatedLoginResponse.from_mapping(data).normalize()
