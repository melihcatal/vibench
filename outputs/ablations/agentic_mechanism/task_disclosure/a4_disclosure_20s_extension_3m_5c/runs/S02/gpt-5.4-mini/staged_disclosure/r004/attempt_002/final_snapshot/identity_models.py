from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any, Mapping, Optional
from urllib.parse import urlparse


def _clean_str(value: Any) -> Optional[str]:
    if value is None:
        return None
    if isinstance(value, str):
        value = value.strip()
        return value or None
    return str(value).strip() or None


def _first_present(data: Mapping[str, Any], *keys: str) -> Any:
    for key in keys:
        if key in data and data[key] is not None:
            return data[key]
    return None


def _parse_datetime(value: Any) -> Optional[datetime]:
    text = _clean_str(value)
    if not text:
        return None
    try:
        parsed = datetime.fromisoformat(text.replace("Z", "+00:00"))
    except ValueError:
        return None
    if parsed.tzinfo is None:
        parsed = parsed.replace(tzinfo=timezone.utc)
    return parsed.astimezone(timezone.utc)


def _normalize_provider_name(value: Any) -> Optional[str]:
    name = _clean_str(value)
    return name.lower() if name else None


def _normalize_subject(value: Any) -> Optional[str]:
    return _clean_str(value)


def _normalize_email(value: Any) -> Optional[str]:
    email = _clean_str(value)
    return email.lower() if email else None


def _normalize_issuer(value: Any) -> Optional[str]:
    issuer = _clean_str(value)
    if not issuer:
        return None
    parsed = urlparse(issuer)
    if parsed.scheme and parsed.netloc:
        return issuer.rstrip("/")
    return issuer


@dataclass(frozen=True)
class FederatedLoginRequest:
    provider: str
    id_token: Optional[str] = None
    access_token: Optional[str] = None
    authorization_code: Optional[str] = None
    redirect_uri: Optional[str] = None
    nonce: Optional[str] = None
    state: Optional[str] = None
    scopes: tuple[str, ...] = field(default_factory=tuple)

    @classmethod
    def from_dict(cls, data: Mapping[str, Any]) -> "FederatedLoginRequest":
        return cls(
            provider=_clean_str(_first_present(data, "provider", "provider_name")) or "",
            id_token=_clean_str(_first_present(data, "id_token", "idToken")),
            access_token=_clean_str(_first_present(data, "access_token", "accessToken")),
            authorization_code=_clean_str(_first_present(data, "authorization_code", "code")),
            redirect_uri=_clean_str(_first_present(data, "redirect_uri", "redirectUri")),
            nonce=_clean_str(data.get("nonce")),
            state=_clean_str(data.get("state")),
            scopes=tuple(
                _clean_str(scope)
                for scope in (data.get("scopes") or ())
                if _clean_str(scope)
            ),
        )

    def normalized_provider(self) -> str:
        provider = _normalize_provider_name(self.provider)
        if not provider:
            raise ValueError("provider is required")
        return provider


@dataclass(frozen=True)
class FederatedIdentity:
    provider: str
    subject: str
    email: Optional[str] = None
    email_verified: Optional[bool] = None
    display_name: Optional[str] = None
    given_name: Optional[str] = None
    family_name: Optional[str] = None
    picture_url: Optional[str] = None
    issuer: Optional[str] = None
    audience: Optional[str] = None
    expires_at: Optional[datetime] = None
    raw_claims: Mapping[str, Any] = field(default_factory=dict)

    @classmethod
    def from_dict(cls, data: Mapping[str, Any]) -> "FederatedIdentity":
        return cls(
            provider=_normalize_provider_name(_first_present(data, "provider", "provider_name")) or "",
            subject=_normalize_subject(_first_present(data, "subject", "sub")) or "",
            email=_normalize_email(_first_present(data, "email", "email_address")),
            email_verified=data.get("email_verified"),
            display_name=_clean_str(_first_present(data, "display_name", "name")),
            given_name=_clean_str(data.get("given_name")),
            family_name=_clean_str(data.get("family_name")),
            picture_url=_clean_str(_first_present(data, "picture_url", "picture")),
            issuer=_normalize_issuer(_first_present(data, "issuer", "iss")),
            audience=_clean_str(_first_present(data, "audience", "aud")),
            expires_at=_parse_datetime(_first_present(data, "expires_at", "exp")),
            raw_claims=dict(data),
        )

    def normalized(self) -> "FederatedIdentity":
        provider = _normalize_provider_name(self.provider)
        subject = _normalize_subject(self.subject)
        if not provider:
            raise ValueError("provider is required")
        if not subject:
            raise ValueError("subject is required")
        return FederatedIdentity(
            provider=provider,
            subject=subject,
            email=_normalize_email(self.email),
            email_verified=self.email_verified,
            display_name=_clean_str(self.display_name),
            given_name=_clean_str(self.given_name),
            family_name=_clean_str(self.family_name),
            picture_url=_clean_str(self.picture_url),
            issuer=_normalize_issuer(self.issuer),
            audience=_clean_str(self.audience),
            expires_at=self.expires_at.astimezone(timezone.utc) if self.expires_at else None,
            raw_claims=dict(self.raw_claims),
        )


@dataclass(frozen=True)
class FederatedLoginResponse:
    identity: FederatedIdentity
    session_token: Optional[str] = None
    refresh_token: Optional[str] = None
    expires_at: Optional[datetime] = None
    issued_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))

    @classmethod
    def from_dict(cls, data: Mapping[str, Any]) -> "FederatedLoginResponse":
        identity_data = data.get("identity") or data
        return cls(
            identity=FederatedIdentity.from_dict(identity_data).normalized(),
            session_token=_clean_str(_first_present(data, "session_token", "sessionToken")),
            refresh_token=_clean_str(_first_present(data, "refresh_token", "refreshToken")),
            expires_at=_parse_datetime(_first_present(data, "expires_at", "expiresAt")),
            issued_at=_parse_datetime(_first_present(data, "issued_at", "issuedAt")) or datetime.now(timezone.utc),
        )

    def normalized(self) -> "FederatedLoginResponse":
        return FederatedLoginResponse(
            identity=self.identity.normalized(),
            session_token=_clean_str(self.session_token),
            refresh_token=_clean_str(self.refresh_token),
            expires_at=self.expires_at.astimezone(timezone.utc) if self.expires_at else None,
            issued_at=self.issued_at.astimezone(timezone.utc),
        )
