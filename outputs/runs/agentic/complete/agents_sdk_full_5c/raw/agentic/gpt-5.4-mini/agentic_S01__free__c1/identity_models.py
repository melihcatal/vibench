from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict, Optional


@dataclass
class EmailPasswordRequest:
    email: str
    password: str

    def normalized(self) -> Dict[str, str]:
        return {"email": self.email.strip().lower(), "password": self.password}


@dataclass
class TokenResponse:
    access_token: str
    refresh_token: Optional[str] = None
    expires_in: Optional[int] = None


def normalize_email(value: str) -> str:
    return value.strip().lower()


def extract_tokens(payload: Dict[str, Any]) -> TokenResponse:
    token = payload.get("session") or payload.get("tokens") or payload
    return TokenResponse(
        access_token=token.get("access_token") or token.get("jwt") or "",
        refresh_token=token.get("refresh_token"),
        expires_in=token.get("expires_in"),
    )
