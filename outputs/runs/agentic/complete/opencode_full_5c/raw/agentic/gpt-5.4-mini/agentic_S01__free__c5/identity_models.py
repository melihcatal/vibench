from dataclasses import asdict, dataclass
from typing import Any, Dict, Optional


@dataclass
class RegisterUserRequest:
    email: str
    password: str
    connection: Optional[str] = None
    given_name: Optional[str] = None
    family_name: Optional[str] = None


@dataclass
class LoginRequest:
    email: str
    password: str
    realm: Optional[str] = None


@dataclass
class RefreshRequest:
    refresh_token: str


@dataclass
class PasswordResetRequest:
    email: str
    connection: Optional[str] = None


def to_payload(model: Any) -> Dict[str, Any]:
    return {k: v for k, v in asdict(model).items() if v is not None}


def extract_tokens(response: Dict[str, Any]) -> Dict[str, Any]:
    return {
        "access_token": response.get("access_token"),
        "refresh_token": response.get("refresh_token"),
        "id_token": response.get("id_token"),
        "token_type": response.get("token_type"),
        "expires_in": response.get("expires_in"),
    }
