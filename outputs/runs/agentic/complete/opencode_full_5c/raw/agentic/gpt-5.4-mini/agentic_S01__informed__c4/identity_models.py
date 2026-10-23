from dataclasses import dataclass
from typing import Any


@dataclass
class RegisterUserRequest:
    email: str
    password: str
    display_name: str | None = None


@dataclass
class LoginRequest:
    email: str
    password: str


@dataclass
class RefreshSessionRequest:
    refresh_token: str | None = None
    access_token: str | None = None


@dataclass
class PasswordResetRequest:
    email: str


@dataclass
class RegisterUserResponse:
    user_id: str | None
    email: str | None
    raw: dict[str, Any]

    @classmethod
    def from_user(cls, user: dict[str, Any]) -> "RegisterUserResponse":
        return cls(user_id=user.get("user_id") or user.get("id"), email=user.get("email"), raw=user)

    def to_dict(self) -> dict[str, Any]:
        return {"user_id": self.user_id, "email": self.email, "raw": self.raw}


@dataclass
class LoginResponse:
    access_token: str | None
    refresh_token: str | None
    token_type: str | None
    raw: dict[str, Any]

    @classmethod
    def from_session(cls, session: dict[str, Any]) -> "LoginResponse":
        return cls(access_token=session.get("access_token"), refresh_token=session.get("refresh_token"), token_type=session.get("token_type"), raw=session)

    def to_dict(self) -> dict[str, Any]:
        return {"access_token": self.access_token, "refresh_token": self.refresh_token, "token_type": self.token_type, "raw": self.raw}


@dataclass
class RefreshSessionResponse:
    access_token: str | None
    refresh_token: str | None
    token_type: str | None
    raw: dict[str, Any]

    @classmethod
    def from_session(cls, session: dict[str, Any]) -> "RefreshSessionResponse":
        return cls(access_token=session.get("access_token"), refresh_token=session.get("refresh_token"), token_type=session.get("token_type"), raw=session)

    def to_dict(self) -> dict[str, Any]:
        return {"access_token": self.access_token, "refresh_token": self.refresh_token, "token_type": self.token_type, "raw": self.raw}


@dataclass
class PasswordResetResponse:
    message: str | None
    raw: dict[str, Any]

    @classmethod
    def from_result(cls, result: dict[str, Any]) -> "PasswordResetResponse":
        return cls(message=result.get("message") if isinstance(result, dict) else str(result), raw=result if isinstance(result, dict) else {"result": result})

    def to_dict(self) -> dict[str, Any]:
        return {"message": self.message, "raw": self.raw}
