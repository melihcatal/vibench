from dataclasses import dataclass
from typing import Any, Dict, Optional


def normalize_email(email: str) -> str:
    return email.strip().lower()


def normalize_locale(locale: Optional[str]) -> str:
    if not locale:
        return "en-US"
    return locale.replace("_", "-").strip()


def normalize_text(value: Optional[str]) -> str:
    return "" if value is None else value.strip()


@dataclass
class AccountRequest:
    email: str
    password: Optional[str] = None
    locale: Optional[str] = None

    def to_dict(self) -> Dict[str, Any]:
        data: Dict[str, Any] = {"email": normalize_email(self.email)}
        if self.password is not None:
            data["password"] = self.password
        if self.locale is not None:
            data["locale"] = normalize_locale(self.locale)
        return data


@dataclass
class TokenResponse:
    access_token: str
    refresh_token: Optional[str] = None
    expires_in: Optional[int] = None
    id_token: Optional[str] = None

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "TokenResponse":
        return cls(
            access_token=data.get("access_token") or data.get("accessToken") or "",
            refresh_token=data.get("refresh_token") or data.get("refreshToken"),
            expires_in=data.get("expires_in") or data.get("expiresIn"),
            id_token=data.get("id_token") or data.get("idToken"),
        )


@dataclass
class ServiceResult:
    ok: bool
    data: Dict[str, Any]
    provider: str
