from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any, Mapping, Optional
from urllib.parse import urlparse


def _coerce_str(value: Any) -> Optional[str]:
    if value is None:
        return None
    if isinstance(value, str):
        value = value.strip()
        return value or None
    return str(value)


def _coerce_bool(value: Any) -> Optional[bool]:
    if value is None or isinstance(value, bool):
        return value
    if isinstance(value, (int, float)):
        return bool(value)
    if isinstance(value, str):
        normalized = value.strip().lower()
        if normalized in {"1", "true", "yes", "y", "on"}:
            return True
        if normalized in {"0", "false", "no", "n", "off"}:
            return False
    return None


def _coerce_int(value: Any) -> Optional[int]:
    if value is None:
        return None
    if isinstance(value, bool):
        return int(value)
    if isinstance(value, int):
        return value
    if isinstance(value, str):
        value = value.strip()
        if not value:
            return None
        try:
            return int(value)
        except ValueError:
            return None
    return None


def _coerce_url(value: Any) -> Optional[str]:
    text = _coerce_str(value)
    if not text:
        return None
    parsed = urlparse(text)
    if parsed.scheme and parsed.netloc:
        return text
    return None


def _coerce_datetime(value: Any) -> Optional[datetime]:
    if value is None:
        return None
    if isinstance(value, datetime):
        return value if value.tzinfo else value.replace(tzinfo=timezone.utc)
    text = _coerce_str(value)
    if not text:
        return None
    if text.endswith("Z"):
        text = text[:-1] + "+00:00"
    try:
        dt = datetime.fromisoformat(text)
    except ValueError:
        return None
    return dt if dt.tzinfo else dt.replace(tzinfo=timezone.utc)


@dataclass(frozen=True)
class OAuthAuthorizationRequest:
    client_id: str
    redirect_uri: str
    scope: str
    response_type: str = "code"
    state: Optional[str] = None
    code_challenge: Optional[str] = None
    code_challenge_method: Optional[str] = None
    prompt: Optional[str] = None
    login_hint: Optional[str] = None
    additional_parameters: Mapping[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        data = {
            "client_id": self.client_id,
            "redirect_uri": self.redirect_uri,
            "scope": self.scope,
            "response_type": self.response_type,
        }
        optional = {
            "state": self.state,
            "code_challenge": self.code_challenge,
            "code_challenge_method": self.code_challenge_method,
            "prompt": self.prompt,
            "login_hint": self.login_hint,
        }
        data.update({k: v for k, v in optional.items() if v is not None})
        data.update(dict(self.additional_parameters))
        return data


@dataclass(frozen=True)
class OAuthTokenRequest:
    grant_type: str
    client_id: Optional[str] = None
    client_secret: Optional[str] = None
    code: Optional[str] = None
    redirect_uri: Optional[str] = None
    code_verifier: Optional[str] = None
    refresh_token: Optional[str] = None
    additional_parameters: Mapping[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        data = {"grant_type": self.grant_type}
        optional = {
            "client_id": self.client_id,
            "client_secret": self.client_secret,
            "code": self.code,
            "redirect_uri": self.redirect_uri,
            "code_verifier": self.code_verifier,
            "refresh_token": self.refresh_token,
        }
        data.update({k: v for k, v in optional.items() if v is not None})
        data.update(dict(self.additional_parameters))
        return data


@dataclass(frozen=True)
class OAuthTokenResponse:
    access_token: Optional[str] = None
    token_type: Optional[str] = None
    expires_in: Optional[int] = None
    refresh_token: Optional[str] = None
    scope: Optional[str] = None
    id_token: Optional[str] = None
    raw: Mapping[str, Any] = field(default_factory=dict)

    @classmethod
    def from_mapping(cls, payload: Mapping[str, Any]) -> "OAuthTokenResponse":
        return cls(
            access_token=_coerce_str(payload.get("access_token")),
            token_type=_coerce_str(payload.get("token_type")),
            expires_in=_coerce_int(payload.get("expires_in")),
            refresh_token=_coerce_str(payload.get("refresh_token")),
            scope=_coerce_str(payload.get("scope")),
            id_token=_coerce_str(payload.get("id_token")),
            raw=dict(payload),
        )


@dataclass(frozen=True)
class FederatedUserClaims:
    subject: Optional[str] = None
    issuer: Optional[str] = None
    email: Optional[str] = None
    email_verified: Optional[bool] = None
    given_name: Optional[str] = None
    family_name: Optional[str] = None
    full_name: Optional[str] = None
    preferred_username: Optional[str] = None
    picture: Optional[str] = None
    locale: Optional[str] = None
    updated_at: Optional[datetime] = None
    raw: Mapping[str, Any] = field(default_factory=dict)

    @classmethod
    def normalize(cls, payload: Mapping[str, Any]) -> "FederatedUserClaims":
        full_name = _coerce_str(payload.get("name"))
        given_name = _coerce_str(payload.get("given_name"))
        family_name = _coerce_str(payload.get("family_name"))
        if not full_name and (given_name or family_name):
            full_name = " ".join(part for part in [given_name, family_name] if part)
        return cls(
            subject=_coerce_str(payload.get("sub")),
            issuer=_coerce_str(payload.get("iss")),
            email=_coerce_str(payload.get("email")),
            email_verified=_coerce_bool(payload.get("email_verified")),
            given_name=given_name,
            family_name=family_name,
            full_name=full_name,
            preferred_username=_coerce_str(payload.get("preferred_username")),
            picture=_coerce_url(payload.get("picture")),
            locale=_coerce_str(payload.get("locale")),
            updated_at=_coerce_datetime(payload.get("updated_at")),
            raw=dict(payload),
        )


@dataclass(frozen=True)
class IdentityProfile:
    user_id: Optional[str] = None
    display_name: Optional[str] = None
    email: Optional[str] = None
    is_verified: Optional[bool] = None
    issuer: Optional[str] = None
    subject: Optional[str] = None
    claims: Mapping[str, Any] = field(default_factory=dict)

    @classmethod
    def from_claims(cls, claims: Mapping[str, Any]) -> "IdentityProfile":
        normalized = FederatedUserClaims.normalize(claims)
        return cls(
            user_id=normalized.subject,
            display_name=normalized.full_name or normalized.preferred_username or normalized.email,
            email=normalized.email,
            is_verified=normalized.email_verified,
            issuer=normalized.issuer,
            subject=normalized.subject,
            claims=normalized.raw,
        )


def normalize_authorization_response(payload: Mapping[str, Any]) -> dict[str, Any]:
    return {
        "code": _coerce_str(payload.get("code")),
        "state": _coerce_str(payload.get("state")),
        "session_state": _coerce_str(payload.get("session_state")),
        "iss": _coerce_str(payload.get("iss")),
        "client_id": _coerce_str(payload.get("client_id")),
    }


def normalize_token_response(payload: Mapping[str, Any]) -> OAuthTokenResponse:
    return OAuthTokenResponse.from_mapping(payload)


def normalize_user_claims(payload: Mapping[str, Any]) -> FederatedUserClaims:
    return FederatedUserClaims.normalize(payload)
