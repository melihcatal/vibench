from dataclasses import dataclass
from typing import Any, Dict, Optional


def _norm_email(value: str) -> str:
    return value.strip().lower()


def _norm_locale(value: Optional[str]) -> str:
    return (value or "en").strip().replace("_", "-")


@dataclass
class UserIdentityRequest:
    email: str
    password: Optional[str] = None
    locale: Optional[str] = None
    display_name: Optional[str] = None

    def normalized(self) -> Dict[str, Any]:
        return {
            "email": _norm_email(self.email),
            "password": self.password,
            "locale": _norm_locale(self.locale),
            "display_name": self.display_name.strip() if self.display_name else None,
        }


@dataclass
class TokenResponse:
    access_token: str
    refresh_token: Optional[str] = None
    expires_in: Optional[int] = None
    token_type: str = "Bearer"

    def as_dict(self) -> Dict[str, Any]:
        return {
            "access_token": self.access_token,
            "refresh_token": self.refresh_token,
            "expires_in": self.expires_in,
            "token_type": self.token_type,
        }


def coerce_response(data: Dict[str, Any]) -> Dict[str, Any]:
    out = dict(data)
    if "email" in out and isinstance(out["email"], str):
        out["email"] = _norm_email(out["email"])
    if "locale" in out:
        out["locale"] = _norm_locale(out.get("locale"))
    return out
