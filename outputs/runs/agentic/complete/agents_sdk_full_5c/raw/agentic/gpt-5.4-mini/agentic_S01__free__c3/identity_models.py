from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict, Optional


@dataclass
class EmailPasswordRequest:
    email: str
    password: str

    def normalized_email(self) -> str:
        return self.email.strip().lower()


@dataclass
class TokenResponse:
    access_token: str
    refresh_token: Optional[str] = None
    id_token: Optional[str] = None
    expires_in: Optional[int] = None
    token_type: Optional[str] = None

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "TokenResponse":
        return cls(
            access_token=data.get("access_token", ""),
            refresh_token=data.get("refresh_token"),
            id_token=data.get("id_token"),
            expires_in=data.get("expires_in"),
            token_type=data.get("token_type"),
        )


@dataclass
class ResetRequest:
    email: str

    def normalized_email(self) -> str:
        return self.email.strip().lower()


@dataclass
class LifecycleResult:
    success: bool
    details: Dict[str, Any]
