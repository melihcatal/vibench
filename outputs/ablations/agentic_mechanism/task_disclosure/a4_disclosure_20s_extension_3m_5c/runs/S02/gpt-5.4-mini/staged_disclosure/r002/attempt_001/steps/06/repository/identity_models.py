from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any, Mapping, Optional


def _normalize_str(value: Any) -> Optional[str]:
    if value is None:
        return None
    text = str(value).strip()
    return text or None


def _normalize_bool(value: Any) -> Optional[bool]:
    if value is None or isinstance(value, bool):
        return value
    if isinstance(value, str):
        lowered = value.strip().lower()
        if lowered in {"true", "1", "yes", "y", "on"}:
            return True
        if lowered in {"false", "0", "no", "n", "off"}:
            return False
    if isinstance(value, (int, float)):
        return bool(value)
    return None


def _normalize_int(value: Any) -> Optional[int]:
    if value is None or isinstance(value, int):
        return value
    if isinstance(value, str):
        text = value.strip()
        if not text:
            return None
        try:
            return int(text)
        except ValueError:
            return None
    return None


def _normalize_timestamp(value: Any) -> Optional[datetime]:
    if value is None:
        return None
    if isinstance(value, datetime):
        return value if value.tzinfo else value.replace(tzinfo=timezone.utc)
    if isinstance(value, (int, float)):
        return datetime.fromtimestamp(value, tz=timezone.utc)
    if isinstance(value, str):
        text = value.strip()
        if not text:
            return None
        try:
            parsed = datetime.fromisoformat(text.replace("Z", "+00:00"))
            return parsed if parsed.tzinfo else parsed.replace(tzinfo=timezone.utc)
        except ValueError:
            return None
    return None


@dataclass(frozen=True)
class FederatedLoginRequest:
    provider: str
    token: str
    redirect_uri: Optional[str] = None
    state: Optional[str] = None
    code_verifier: Optional[str] = None
    nonce: Optional[str] = None
    scopes: tuple[str, ...] = field(default_factory=tuple)

    @classmethod
    def from_mapping(cls, data: Mapping[str, Any]) -> "FederatedLoginRequest":
        scopes = data.get("scopes") or ()
        if isinstance(scopes, str):
            scopes = tuple(part for part in scopes.split() if part)
        else:
            scopes = tuple(_normalize_str(item) for item in scopes if _normalize_str(item))
        return cls(
            provider=_normalize_str(data.get("provider")) or "",
            token=_normalize_str(data.get("token")) or "",
            redirect_uri=_normalize_str(data.get("redirect_uri")),
            state=_normalize_str(data.get("state")),
            code_verifier=_normalize_str(data.get("code_verifier")),
            nonce=_normalize_str(data.get("nonce")),
            scopes=scopes,
        )


@dataclass(frozen=True)
class FederatedLoginResponse:
    subject: str
    email: Optional[str] = None
    email_verified: Optional[bool] = None
    full_name: Optional[str] = None
    given_name: Optional[str] = None
    family_name: Optional[str] = None
    picture_url: Optional[str] = None
    issuer: Optional[str] = None
    audience: Optional[str] = None
    access_token: Optional[str] = None
    refresh_token: Optional[str] = None
    expires_in: Optional[int] = None
    issued_at: Optional[datetime] = None
    raw: Mapping[str, Any] = field(default_factory=dict)

    @classmethod
    def from_mapping(cls, data: Mapping[str, Any]) -> "FederatedLoginResponse":
        return cls(
            subject=_normalize_str(data.get("subject") or data.get("sub")) or "",
            email=_normalize_str(data.get("email")),
            email_verified=_normalize_bool(data.get("email_verified")),
            full_name=_normalize_str(data.get("full_name") or data.get("name")),
            given_name=_normalize_str(data.get("given_name")),
            family_name=_normalize_str(data.get("family_name")),
            picture_url=_normalize_str(data.get("picture_url") or data.get("picture")),
            issuer=_normalize_str(data.get("issuer") or data.get("iss")),
            audience=_normalize_str(data.get("audience") or data.get("aud")),
            access_token=_normalize_str(data.get("access_token")),
            refresh_token=_normalize_str(data.get("refresh_token")),
            expires_in=_normalize_int(data.get("expires_in")),
            issued_at=_normalize_timestamp(data.get("issued_at") or data.get("iat")),
            raw=dict(data),
        )


def normalize_federated_identity(data: Mapping[str, Any]) -> dict[str, Any]:
    request = FederatedLoginRequest.from_mapping(data)
    response = FederatedLoginResponse.from_mapping(data)
    return {
        "request": request,
        "response": response,
        "provider": request.provider or response.issuer,
        "subject": response.subject,
        "email": response.email,
        "display_name": response.full_name,
        "verified": response.email_verified,
        "token_present": bool(request.token),
    }
