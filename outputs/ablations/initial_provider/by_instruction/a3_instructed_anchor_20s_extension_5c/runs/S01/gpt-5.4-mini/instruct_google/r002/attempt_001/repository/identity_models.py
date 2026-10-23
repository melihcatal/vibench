from dataclasses import dataclass, field
from typing import Any, Dict, Optional


def normalize_email(value: str) -> str:
    return value.strip().lower()


def normalize_locale(value: Optional[str]) -> str:
    if not value:
        return "en"
    return value.replace("_", "-").strip().lower()


@dataclass
class AccountInput:
    email: str
    password: str
    locale: str = "en"
    display_name: Optional[str] = None
    metadata: Dict[str, Any] = field(default_factory=dict)

    def normalized(self) -> "AccountInput":
        return AccountInput(
            email=normalize_email(self.email),
            password=self.password,
            locale=normalize_locale(self.locale),
            display_name=self.display_name.strip() if self.display_name else None,
            metadata=dict(self.metadata),
        )


@dataclass
class AuthSession:
    access_token: str
    refresh_token: Optional[str] = None
    expires_in: Optional[int] = None
    token_type: str = "Bearer"
    user_id: Optional[str] = None


@dataclass
class LifecycleResponse:
    ok: bool
    data: Dict[str, Any] = field(default_factory=dict)
    error: Optional[str] = None
