from dataclasses import dataclass
from typing import Any, Dict, Optional


def normalize_email(email: str) -> str:
    return email.strip().lower()


@dataclass
class RegisterUserRequest:
    email: str
    password: str
    display_name: Optional[str] = None

    def normalized(self) -> Dict[str, Any]:
        payload = {"email": normalize_email(self.email), "password": self.password}
        if self.display_name is not None:
            payload["displayName"] = self.display_name.strip()
        return payload


@dataclass
class LoginRequest:
    email: str
    password: str

    def normalized(self) -> Dict[str, Any]:
        return {"email": normalize_email(self.email), "password": self.password}


@dataclass
class RefreshRequest:
    refresh_token: str

    def normalized(self) -> Dict[str, Any]:
        return {"refresh_token": self.refresh_token}


@dataclass
class PasswordResetRequest:
    email: str

    def normalized(self) -> Dict[str, Any]:
        return {"email": normalize_email(self.email)}


@dataclass
class IdentityResult:
    status: str
    data: Dict[str, Any]
