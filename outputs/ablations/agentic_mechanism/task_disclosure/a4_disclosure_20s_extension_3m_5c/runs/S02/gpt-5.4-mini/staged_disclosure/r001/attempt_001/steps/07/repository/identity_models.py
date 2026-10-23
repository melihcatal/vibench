from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Mapping, Optional
from urllib.parse import urlparse


def _coerce_str(value: Any, *, field_name: str, allow_empty: bool = False) -> str:
    if value is None:
        raise ValueError(f"{field_name} is required")
    text = str(value).strip()
    if not text and not allow_empty:
        raise ValueError(f"{field_name} cannot be empty")
    return text


def _normalize_url(value: Any, *, field_name: str) -> str:
    text = _coerce_str(value, field_name=field_name)
    parsed = urlparse(text)
    if parsed.scheme not in {"http", "https"} or not parsed.netloc:
        raise ValueError(f"{field_name} must be an absolute http(s) URL")
    return text


def _get(mapping: Mapping[str, Any], *keys: str) -> Any:
    for key in keys:
        if key in mapping:
            return mapping[key]
    return None


@dataclass(frozen=True)
class FederatedLoginRequest:
    provider: str
    redirect_uri: str
    client_id: str
    scope: str = "openid email profile"
    state: Optional[str] = None
    nonce: Optional[str] = None
    login_hint: Optional[str] = None
    prompt: Optional[str] = None
    extra_params: Mapping[str, Any] = field(default_factory=dict)

    @classmethod
    def normalize(cls, data: Mapping[str, Any]) -> "FederatedLoginRequest":
        provider = _coerce_str(_get(data, "provider", "issuer", "identity_provider"), field_name="provider")
        redirect_uri = _normalize_url(_get(data, "redirect_uri", "callback_url"), field_name="redirect_uri")
        client_id = _coerce_str(_get(data, "client_id", "audience"), field_name="client_id")
        scope = _coerce_str(_get(data, "scope"), field_name="scope", allow_empty=False) if _get(data, "scope") is not None else "openid email profile"
        state = _get(data, "state")
        nonce = _get(data, "nonce")
        login_hint = _get(data, "login_hint")
        prompt = _get(data, "prompt")
        extra = dict(_get(data, "extra_params") or {})
        reserved = {"provider", "issuer", "identity_provider", "redirect_uri", "callback_url", "client_id", "audience", "scope", "state", "nonce", "login_hint", "prompt", "extra_params"}
        for key, value in data.items():
            if key not in reserved:
                extra[key] = value
        return cls(
            provider=provider,
            redirect_uri=redirect_uri,
            client_id=client_id,
            scope=scope,
            state=None if state is None else str(state),
            nonce=None if nonce is None else str(nonce),
            login_hint=None if login_hint is None else str(login_hint),
            prompt=None if prompt is None else str(prompt),
            extra_params=extra,
        )

    def to_dict(self) -> dict[str, Any]:
        payload = {
            "provider": self.provider,
            "redirect_uri": self.redirect_uri,
            "client_id": self.client_id,
            "scope": self.scope,
        }
        if self.state is not None:
            payload["state"] = self.state
        if self.nonce is not None:
            payload["nonce"] = self.nonce
        if self.login_hint is not None:
            payload["login_hint"] = self.login_hint
        if self.prompt is not None:
            payload["prompt"] = self.prompt
        if self.extra_params:
            payload["extra_params"] = dict(self.extra_params)
        return payload


@dataclass(frozen=True)
class FederatedLoginResponse:
    provider: str
    authorization_url: str
    state: Optional[str] = None
    nonce: Optional[str] = None
    expires_in: Optional[int] = None
    session_id: Optional[str] = None
    raw: Mapping[str, Any] = field(default_factory=dict)

    @classmethod
    def normalize(cls, data: Mapping[str, Any]) -> "FederatedLoginResponse":
        provider = _coerce_str(_get(data, "provider", "issuer", "identity_provider"), field_name="provider")
        authorization_url = _normalize_url(_get(data, "authorization_url", "auth_url", "url"), field_name="authorization_url")
        expires_in = _get(data, "expires_in")
        if expires_in is not None:
            expires_in = int(expires_in)
        state = _get(data, "state")
        nonce = _get(data, "nonce")
        session_id = _get(data, "session_id")
        return cls(
            provider=provider,
            authorization_url=authorization_url,
            state=None if state is None else str(state),
            nonce=None if nonce is None else str(nonce),
            expires_in=expires_in,
            session_id=None if session_id is None else str(session_id),
            raw=dict(data),
        )

    def to_dict(self) -> dict[str, Any]:
        payload = {
            "provider": self.provider,
            "authorization_url": self.authorization_url,
        }
        if self.state is not None:
            payload["state"] = self.state
        if self.nonce is not None:
            payload["nonce"] = self.nonce
        if self.expires_in is not None:
            payload["expires_in"] = self.expires_in
        if self.session_id is not None:
            payload["session_id"] = self.session_id
        return payload


def normalize_federated_login_request(data: Mapping[str, Any]) -> FederatedLoginRequest:
    return FederatedLoginRequest.normalize(data)


def normalize_federated_login_response(data: Mapping[str, Any]) -> FederatedLoginResponse:
    return FederatedLoginResponse.normalize(data)
