from __future__ import annotations

from dataclasses import dataclass, field, asdict
from datetime import datetime, timezone, timedelta
from typing import Any, Mapping
from urllib.parse import parse_qsl, urlencode


def _utc_now() -> datetime:
    return datetime.now(timezone.utc)


def _normalize_str(value: Any) -> str:
    if value is None:
        return ""
    if isinstance(value, str):
        return value.strip()
    return str(value).strip()


def _normalize_email(value: Any) -> str:
    return _normalize_str(value).lower()


def _normalize_bool(value: Any) -> bool:
    if isinstance(value, bool):
        return value
    if value is None:
        return False
    if isinstance(value, (int, float)):
        return value != 0
    text = _normalize_str(value).lower()
    return text in {"1", "true", "t", "yes", "y", "on"}


def _normalize_scopes(value: Any) -> list[str]:
    if value is None:
        return []
    if isinstance(value, str):
        parts = value.replace(",", " ").split()
        return [part.strip() for part in parts if part.strip()]
    if isinstance(value, (list, tuple, set)):
        return [s for s in (_normalize_str(item) for item in value) if s]
    return [_normalize_str(value)]


def _normalize_mapping(data: Mapping[str, Any]) -> dict[str, Any]:
    return {str(key): value for key, value in data.items()}


@dataclass(frozen=True)
class AuthorizationRequest:
    client_id: str
    redirect_uri: str
    response_type: str = "code"
    scope: tuple[str, ...] = ()
    state: str = ""
    code_challenge: str = ""
    code_challenge_method: str = "S256"
    nonce: str = ""
    prompt: str = ""
    acr_values: str = ""
    extra_params: dict[str, Any] = field(default_factory=dict)

    def normalized(self) -> "AuthorizationRequest":
        return AuthorizationRequest(
            client_id=_normalize_str(self.client_id),
            redirect_uri=_normalize_str(self.redirect_uri),
            response_type=_normalize_str(self.response_type) or "code",
            scope=tuple(_normalize_scopes(self.scope)),
            state=_normalize_str(self.state),
            code_challenge=_normalize_str(self.code_challenge),
            code_challenge_method=_normalize_str(self.code_challenge_method) or "S256",
            nonce=_normalize_str(self.nonce),
            prompt=_normalize_str(self.prompt),
            acr_values=_normalize_str(self.acr_values),
            extra_params=_normalize_mapping(self.extra_params),
        )

    def to_query(self) -> str:
        normalized = self.normalized()
        params: list[tuple[str, str]] = [
            ("client_id", normalized.client_id),
            ("redirect_uri", normalized.redirect_uri),
            ("response_type", normalized.response_type),
        ]
        if normalized.scope:
            params.append(("scope", " ".join(normalized.scope)))
        if normalized.state:
            params.append(("state", normalized.state))
        if normalized.code_challenge:
            params.append(("code_challenge", normalized.code_challenge))
        if normalized.code_challenge_method:
            params.append(("code_challenge_method", normalized.code_challenge_method))
        if normalized.nonce:
            params.append(("nonce", normalized.nonce))
        if normalized.prompt:
            params.append(("prompt", normalized.prompt))
        if normalized.acr_values:
            params.append(("acr_values", normalized.acr_values))
        params.extend((str(k), _normalize_str(v)) for k, v in normalized.extra_params.items())
        return urlencode(params)


@dataclass(frozen=True)
class TokenRequest:
    grant_type: str = "authorization_code"
    code: str = ""
    redirect_uri: str = ""
    client_id: str = ""
    client_secret: str = ""
    code_verifier: str = ""
    refresh_token: str = ""
    scope: tuple[str, ...] = ()
    extra_params: dict[str, Any] = field(default_factory=dict)

    def normalized(self) -> "TokenRequest":
        return TokenRequest(
            grant_type=_normalize_str(self.grant_type) or "authorization_code",
            code=_normalize_str(self.code),
            redirect_uri=_normalize_str(self.redirect_uri),
            client_id=_normalize_str(self.client_id),
            client_secret=_normalize_str(self.client_secret),
            code_verifier=_normalize_str(self.code_verifier),
            refresh_token=_normalize_str(self.refresh_token),
            scope=tuple(_normalize_scopes(self.scope)),
            extra_params=_normalize_mapping(self.extra_params),
        )

    def to_form(self) -> dict[str, str]:
        normalized = self.normalized()
        form: dict[str, str] = {"grant_type": normalized.grant_type}
        if normalized.code:
            form["code"] = normalized.code
        if normalized.redirect_uri:
            form["redirect_uri"] = normalized.redirect_uri
        if normalized.client_id:
            form["client_id"] = normalized.client_id
        if normalized.client_secret:
            form["client_secret"] = normalized.client_secret
        if normalized.code_verifier:
            form["code_verifier"] = normalized.code_verifier
        if normalized.refresh_token:
            form["refresh_token"] = normalized.refresh_token
        if normalized.scope:
            form["scope"] = " ".join(normalized.scope)
        for key, value in normalized.extra_params.items():
            form[str(key)] = _normalize_str(value)
        return form


@dataclass(frozen=True)
class TokenResponse:
    access_token: str = ""
    token_type: str = "Bearer"
    expires_in: int = 0
    refresh_token: str = ""
    id_token: str = ""
    scope: tuple[str, ...] = ()
    issued_at: datetime = field(default_factory=_utc_now)
    raw: dict[str, Any] = field(default_factory=dict)

    @classmethod
    def from_mapping(cls, data: Mapping[str, Any]) -> "TokenResponse":
        mapping = _normalize_mapping(data)
        return cls(
            access_token=_normalize_str(mapping.get("access_token")),
            token_type=_normalize_str(mapping.get("token_type")) or "Bearer",
            expires_in=int(mapping.get("expires_in") or 0),
            refresh_token=_normalize_str(mapping.get("refresh_token")),
            id_token=_normalize_str(mapping.get("id_token")),
            scope=tuple(_normalize_scopes(mapping.get("scope"))),
            issued_at=_utc_now(),
            raw=dict(mapping),
        )

    def expires_at(self) -> datetime | None:
        if self.expires_in <= 0:
            return None
        return self.issued_at + timedelta(seconds=self.expires_in)


@dataclass(frozen=True)
class FederatedUserProfile:
    subject: str = ""
    email: str = ""
    email_verified: bool = False
    full_name: str = ""
    given_name: str = ""
    family_name: str = ""
    picture: str = ""
    locale: str = ""
    raw: dict[str, Any] = field(default_factory=dict)

    @classmethod
    def from_claims(cls, claims: Mapping[str, Any]) -> "FederatedUserProfile":
        mapping = _normalize_mapping(claims)
        return cls(
            subject=_normalize_str(mapping.get("sub")),
            email=_normalize_email(mapping.get("email")),
            email_verified=_normalize_bool(mapping.get("email_verified")),
            full_name=_normalize_str(mapping.get("name")),
            given_name=_normalize_str(mapping.get("given_name")),
            family_name=_normalize_str(mapping.get("family_name")),
            picture=_normalize_str(mapping.get("picture")),
            locale=_normalize_str(mapping.get("locale")),
            raw=dict(mapping),
        )

    def display_name(self) -> str:
        if self.full_name:
            return self.full_name
        pieces = [part for part in (self.given_name, self.family_name) if part]
        if pieces:
            return " ".join(pieces)
        return self.email or self.subject


@dataclass(frozen=True)
class LoginState:
    state: str
    nonce: str = ""
    code_verifier: str = ""
    created_at: datetime = field(default_factory=_utc_now)
    metadata: dict[str, Any] = field(default_factory=dict)

    def normalized(self) -> "LoginState":
        return LoginState(
            state=_normalize_str(self.state),
            nonce=_normalize_str(self.nonce),
            code_verifier=_normalize_str(self.code_verifier),
            created_at=self.created_at,
            metadata=_normalize_mapping(self.metadata),
        )


def merge_claims(*claim_sets: Mapping[str, Any]) -> dict[str, Any]:
    merged: dict[str, Any] = {}
    for claims in claim_sets:
        merged.update(_normalize_mapping(claims))
    return merged


def parse_query_params(query: str) -> dict[str, str]:
    return {key: value for key, value in parse_qsl(query, keep_blank_values=True)}


def serialize_model(model: Any) -> dict[str, Any]:
    if hasattr(model, "__dataclass_fields__"):
        return asdict(model)
    raise TypeError("serialize_model expects a dataclass instance")
