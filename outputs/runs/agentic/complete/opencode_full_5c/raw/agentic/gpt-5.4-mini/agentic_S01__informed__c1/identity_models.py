from dataclasses import dataclass, field
from typing import Any, Dict, Optional


def normalize_email(value: str) -> str:
    return value.strip().lower()


def normalize_locale(value: Optional[str]) -> str:
    return (value or "en").replace('_', '-').strip() or "en"


def normalize_text(value: Optional[str]) -> str:
    return " ".join((value or "").strip().split())


def compact_metadata(value: Optional[Dict[str, Any]]) -> Dict[str, Any]:
    return dict(value or {})


@dataclass
class AccountRequest:
    email: str
    password: str
    display_name: Optional[str] = None
    locale: Optional[str] = None
    metadata: Dict[str, Any] = field(default_factory=dict)

    def normalized(self) -> "AccountRequest":
        return AccountRequest(
            email=normalize_email(self.email),
            password=self.password,
            display_name=normalize_text(self.display_name) or None,
            locale=normalize_locale(self.locale),
            metadata=compact_metadata(self.metadata),
        )


@dataclass
class TokenSet:
    access_token: str
    refresh_token: Optional[str] = None
    id_token: Optional[str] = None
    token_type: Optional[str] = None
    expires_in: Optional[int] = None


@dataclass
class SupportNote:
    account_id: str
    locale: str
    summary: str
    metadata: Dict[str, Any] = field(default_factory=dict)
