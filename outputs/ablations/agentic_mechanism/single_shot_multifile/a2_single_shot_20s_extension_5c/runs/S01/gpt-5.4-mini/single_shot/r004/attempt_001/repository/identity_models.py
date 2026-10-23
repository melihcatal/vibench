from dataclasses import dataclass
from typing import Any, Dict, Optional


@dataclass(frozen=True)
class RegisterUserRequest:
    email: str
    password: str
    display_name: Optional[str] = None
    return_secure_token: bool = True

    def to_payload(self) -> Dict[str, Any]:
        payload: Dict[str, Any] = {"email": self.email, "password": self.password, "returnSecureToken": self.return_secure_token}
        if self.display_name:
            payload["displayName"] = self.display_name
        return payload


@dataclass(frozen=True)
class EmailPasswordLoginRequest:
    email: str
    password: str
    return_secure_token: bool = True

    def to_payload(self) -> Dict[str, Any]:
        return {"email": self.email, "password": self.password, "returnSecureToken": self.return_secure_token}


@dataclass(frozen=True)
class PasswordResetRequest:
    email: str
    continue_url: str = ""

    def to_payload(self) -> Dict[str, Any]:
        payload: Dict[str, Any] = {"requestType": "PASSWORD_RESET", "email": self.email}
        if self.continue_url:
            payload["continueUrl"] = self.continue_url
        return payload


def build_register_user_request(email: str, password: str, display_name: Optional[str] = None, return_secure_token: bool = True) -> RegisterUserRequest:
    return RegisterUserRequest(email=email, password=password, display_name=display_name, return_secure_token=return_secure_token)


def build_email_password_login_request(email: str, password: str, return_secure_token: bool = True) -> EmailPasswordLoginRequest:
    return EmailPasswordLoginRequest(email=email, password=password, return_secure_token=return_secure_token)


def build_password_reset_request(email: str, continue_url: str = "") -> PasswordResetRequest:
    return PasswordResetRequest(email=email, continue_url=continue_url)


def normalize_token_response(data: Dict[str, Any]) -> Dict[str, Any]:
    normalized: Dict[str, Any] = dict(data)
    if "idToken" in data:
        normalized["access_token"] = data["idToken"]
    if "refreshToken" in data:
        normalized["refresh_token"] = data["refreshToken"]
    if "expiresIn" in data:
        normalized["expires_in"] = int(data["expiresIn"])
    if "localId" in data:
        normalized["user_id"] = data["localId"]
    if "email" in data:
        normalized["email"] = data["email"]
    return normalized


def normalize_password_reset_response(data: Dict[str, Any]) -> Dict[str, Any]:
    normalized: Dict[str, Any] = dict(data)
    if "email" in data:
        normalized["email"] = data["email"]
    if "kind" in data:
        normalized["provider_kind"] = data["kind"]
    return normalized
