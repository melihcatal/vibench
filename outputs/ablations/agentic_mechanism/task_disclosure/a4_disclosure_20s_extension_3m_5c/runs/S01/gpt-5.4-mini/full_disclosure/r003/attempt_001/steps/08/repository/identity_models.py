from dataclasses import asdict, dataclass, field
from typing import Any, Dict, Mapping, Optional


def _clean_dict(value: Optional[Mapping[str, Any]]) -> Dict[str, Any]:
    return dict(value) if value else {}


def _clean_str(value: Optional[str]) -> Optional[str]:
    if value is None:
        return None
    stripped = value.strip()
    return stripped if stripped else None


def _normalize_email(value: Optional[str]) -> Optional[str]:
    cleaned = _clean_str(value)
    return cleaned.lower() if cleaned else None


@dataclass(frozen=True)
class EmailPasswordRegisterRequest:
    email: str
    password: str
    name: Optional[str] = None
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass(frozen=True)
class EmailPasswordLoginRequest:
    email: str
    password: str


@dataclass(frozen=True)
class PasswordResetRequest:
    email: str
    connection: Optional[str] = None


@dataclass(frozen=True)
class TokenResponse:
    access_token: str
    id_token: Optional[str] = None
    refresh_token: Optional[str] = None
    token_type: str = "Bearer"
    expires_in: Optional[int] = None
    scope: Optional[str] = None


@dataclass(frozen=True)
class IdentityErrorResponse:
    error: str
    description: Optional[str] = None
    status_code: Optional[int] = None


def normalize_email_password_register_request(payload: Mapping[str, Any]) -> EmailPasswordRegisterRequest:
    return EmailPasswordRegisterRequest(
        email=_normalize_email(payload.get("email")) or "",
        password=_clean_str(payload.get("password")) or "",
        name=_clean_str(payload.get("name")),
        metadata=_clean_dict(payload.get("metadata")),
    )


def normalize_email_password_login_request(payload: Mapping[str, Any]) -> EmailPasswordLoginRequest:
    return EmailPasswordLoginRequest(
        email=_normalize_email(payload.get("email")) or "",
        password=_clean_str(payload.get("password")) or "",
    )


def normalize_password_reset_request(payload: Mapping[str, Any]) -> PasswordResetRequest:
    return PasswordResetRequest(
        email=_normalize_email(payload.get("email")) or "",
        connection=_clean_str(payload.get("connection")),
    )


def normalize_token_response(payload: Mapping[str, Any]) -> TokenResponse:
    return TokenResponse(
        access_token=_clean_str(payload.get("access_token")) or "",
        id_token=_clean_str(payload.get("id_token")),
        refresh_token=_clean_str(payload.get("refresh_token")),
        token_type=_clean_str(payload.get("token_type")) or "Bearer",
        expires_in=payload.get("expires_in"),
        scope=_clean_str(payload.get("scope")),
    )


def normalize_identity_error_response(payload: Mapping[str, Any], status_code: Optional[int] = None) -> IdentityErrorResponse:
    return IdentityErrorResponse(
        error=_clean_str(payload.get("error")) or "unknown_error",
        description=_clean_str(payload.get("error_description") or payload.get("description")),
        status_code=status_code,
    )


def request_to_dict(request: Any) -> Dict[str, Any]:
    return asdict(request)
