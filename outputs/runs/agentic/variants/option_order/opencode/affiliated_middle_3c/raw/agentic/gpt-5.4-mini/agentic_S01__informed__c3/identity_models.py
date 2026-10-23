from dataclasses import dataclass
from typing import Any, Dict, Optional

from identity_client import normalize_email, normalize_locale


@dataclass
class RegisterUserRequest:
    email: str
    password: str
    given_name: Optional[str] = None


@dataclass
class LoginRequest:
    email: str
    password: str


@dataclass
class RefreshRequest:
    refresh_token: str


@dataclass
class PasswordResetRequest:
    email: str


def normalize_identity_request(data: Dict[str, Any]) -> Dict[str, Any]:
    normalized = dict(data)
    if "email" in normalized and normalized["email"] is not None:
        normalized["email"] = normalize_email(str(normalized["email"]))
    if "locale" in normalized:
        normalized["locale"] = normalize_locale(normalized.get("locale"))
    return normalized


def parse_auth0_tokens(payload: Dict[str, Any]) -> Dict[str, Any]:
    return {
        "access_token": payload.get("access_token"),
        "id_token": payload.get("id_token"),
        "refresh_token": payload.get("refresh_token"),
        "expires_in": payload.get("expires_in"),
        "token_type": payload.get("token_type"),
    }
