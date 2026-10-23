from dataclasses import dataclass
from typing import Any, Dict, Optional


def normalize_email(email: str) -> str:
    return email.strip().lower()


@dataclass
class UserCredentials:
    email: str
    password: str

    def normalized(self) -> "UserCredentials":
        return UserCredentials(
            email=normalize_email(self.email), password=self.password
        )


@dataclass
class TokenSet:
    access_token: str
    refresh_token: Optional[str] = None
    id_token: Optional[str] = None
    expires_in: Optional[int] = None


@dataclass
class PasswordResetRequest:
    email: str

    def normalized(self) -> "PasswordResetRequest":
        return PasswordResetRequest(email=normalize_email(self.email))


def as_dict(data: Any) -> Dict[str, Any]:
    if hasattr(data, "__dict__"):
        return dict(data.__dict__)
    return dict(data)
