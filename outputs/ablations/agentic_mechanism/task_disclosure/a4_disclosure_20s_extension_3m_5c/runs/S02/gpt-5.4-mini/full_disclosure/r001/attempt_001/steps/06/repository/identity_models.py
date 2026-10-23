from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any, Dict, Mapping, Optional
from uuid import uuid4


def _utc_now() -> datetime:
    return datetime.now(timezone.utc)


def _coerce_str(value: Any) -> Optional[str]:
    if value is None:
        return None
    text = str(value).strip()
    return text or None


def _first_present(mapping: Mapping[str, Any], *keys: str) -> Optional[Any]:
    for key in keys:
        if key in mapping and mapping[key] is not None:
            return mapping[key]
    return None


def _normalize_scope(value: Any) -> list[str]:
    if value is None:
        return []
    if isinstance(value, str):
        parts = value.replace(",", " ").split()
        return [part for part in (p.strip() for p in parts) if part]
    if isinstance(value, (list, tuple, set)):
        normalized = []
        for item in value:
            text = _coerce_str(item)
            if text:
                normalized.append(text)
        return normalized
    text = _coerce_str(value)
    return [text] if text else []


@dataclass(frozen=True)
class FederatedLoginRequest:
    provider: str
    redirect_uri: str
    client_id: Optional[str] = None
    scope: list[str] = field(default_factory=list)
    state: str = field(default_factory=lambda: uuid4().hex)
    nonce: Optional[str] = None
    prompt: Optional[str] = None

    @classmethod
    def from_dict(cls, data: Mapping[str, Any]) -> "FederatedLoginRequest":
        provider = _coerce_str(_first_present(data, "provider", "issuer"))
        redirect_uri = _coerce_str(_first_present(data, "redirect_uri", "redirectUri"))
        if not provider:
            raise ValueError("provider is required")
        if not redirect_uri:
            raise ValueError("redirect_uri is required")
        return cls(
            provider=provider,
            redirect_uri=redirect_uri,
            client_id=_coerce_str(_first_present(data, "client_id", "clientId")),
            scope=_normalize_scope(_first_present(data, "scope", "scopes")),
            state=_coerce_str(_first_present(data, "state")) or uuid4().hex,
            nonce=_coerce_str(_first_present(data, "nonce")),
            prompt=_coerce_str(_first_present(data, "prompt")),
        )

    def to_dict(self) -> Dict[str, Any]:
        payload: Dict[str, Any] = {
            "provider": self.provider,
            "redirect_uri": self.redirect_uri,
            "state": self.state,
        }
        if self.client_id is not None:
            payload["client_id"] = self.client_id
        if self.scope:
            payload["scope"] = self.scope
        if self.nonce is not None:
            payload["nonce"] = self.nonce
        if self.prompt is not None:
            payload["prompt"] = self.prompt
        return payload


@dataclass(frozen=True)
class FederatedTokenResponse:
    access_token: Optional[str] = None
    id_token: Optional[str] = None
    refresh_token: Optional[str] = None
    token_type: Optional[str] = None
    expires_in: Optional[int] = None
    scope: list[str] = field(default_factory=list)
    issued_at: datetime = field(default_factory=_utc_now)

    @classmethod
    def from_dict(cls, data: Mapping[str, Any]) -> "FederatedTokenResponse":
        expires_in = _first_present(data, "expires_in", "expiresIn")
        normalized_expires_in = int(expires_in) if expires_in is not None else None
        return cls(
            access_token=_coerce_str(_first_present(data, "access_token", "accessToken")),
            id_token=_coerce_str(_first_present(data, "id_token", "idToken")),
            refresh_token=_coerce_str(_first_present(data, "refresh_token", "refreshToken")),
            token_type=_coerce_str(_first_present(data, "token_type", "tokenType")),
            expires_in=normalized_expires_in,
            scope=_normalize_scope(_first_present(data, "scope", "scopes")),
            issued_at=_utc_now(),
        )

    def is_expired(self, at: Optional[datetime] = None) -> bool:
        if self.expires_in is None:
            return False
        current = at or _utc_now()
        return (current - self.issued_at).total_seconds() >= self.expires_in

    def to_dict(self) -> Dict[str, Any]:
        payload: Dict[str, Any] = {
            "issued_at": self.issued_at.isoformat(),
        }
        for key in ("access_token", "id_token", "refresh_token", "token_type"):
            value = getattr(self, key)
            if value is not None:
                payload[key] = value
        if self.expires_in is not None:
            payload["expires_in"] = self.expires_in
        if self.scope:
            payload["scope"] = self.scope
        return payload


@dataclass(frozen=True)
class FederatedUserClaims:
    subject: str
    email: Optional[str] = None
    email_verified: Optional[bool] = None
    name: Optional[str] = None
    given_name: Optional[str] = None
    family_name: Optional[str] = None
    picture: Optional[str] = None
    issuer: Optional[str] = None
    raw: Dict[str, Any] = field(default_factory=dict)

    @classmethod
    def from_dict(cls, data: Mapping[str, Any]) -> "FederatedUserClaims":
        subject = _coerce_str(_first_present(data, "sub", "subject"))
        if not subject:
            raise ValueError("subject is required")
        email_verified = _first_present(data, "email_verified", "emailVerified")
        normalized_verified = None if email_verified is None else bool(email_verified)
        return cls(
            subject=subject,
            email=_coerce_str(_first_present(data, "email")),
            email_verified=normalized_verified,
            name=_coerce_str(_first_present(data, "name")),
            given_name=_coerce_str(_first_present(data, "given_name", "givenName")),
            family_name=_coerce_str(_first_present(data, "family_name", "familyName")),
            picture=_coerce_str(_first_present(data, "picture", "avatar_url", "avatarUrl")),
            issuer=_coerce_str(_first_present(data, "iss", "issuer")),
            raw=dict(data),
        )

    def display_name(self) -> str:
        if self.name:
            return self.name
        parts = [part for part in (self.given_name, self.family_name) if part]
        if parts:
            return " ".join(parts)
        return self.subject

    def to_dict(self) -> Dict[str, Any]:
        payload: Dict[str, Any] = {"sub": self.subject, "raw": dict(self.raw)}
        for key in ("email", "name", "given_name", "family_name", "picture", "issuer"):
            value = getattr(self, key)
            if value is not None:
                payload[key] = value
        if self.email_verified is not None:
            payload["email_verified"] = self.email_verified
        return payload


def normalize_claims(data: Mapping[str, Any]) -> FederatedUserClaims:
    return FederatedUserClaims.from_dict(data)


def normalize_token_response(data: Mapping[str, Any]) -> FederatedTokenResponse:
    return FederatedTokenResponse.from_dict(data)
