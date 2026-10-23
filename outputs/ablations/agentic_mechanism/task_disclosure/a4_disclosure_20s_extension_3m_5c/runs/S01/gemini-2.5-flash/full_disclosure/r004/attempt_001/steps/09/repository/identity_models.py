"""
Define local request, response, and normalization helpers for Email/Password Account Lifecycle.
"""

from dataclasses import dataclass
from typing import Optional, Dict, Any

@dataclass
class EmailPasswordLoginRequest:
    email: str
    password: str

@dataclass
class EmailPasswordLoginResponse:
    access_token: str
    refresh_token: str
    token_type: str
    expires_in: int

@dataclass
class RegisterUserRequest:
    email: str
    password: str
    confirm_password: str

@dataclass
class RegisterUserResponse:
    user_id: str
    email: str

@dataclass
class PasswordResetRequest:
    email: str

@dataclass
class PasswordResetResponse:
    message: str

@dataclass
class RefreshSessionRequest:
    refresh_token: str

@dataclass
class RefreshSessionResponse:
    access_token: str
    token_type: str
    expires_in: int

class DataNormalizer:
    @staticmethod
    def normalize_email(email: str) -> str:
        return email.lower().strip()

    @staticmethod
    def sanitize_profile_text(text: str) -> str:
        # Placeholder for profile text moderation/sanitization
        return text.strip()

    @staticmethod
    def to_json(obj: Any) -> Dict[str, Any]:
        if dataclasses.is_dataclass(obj):
            return dataclasses.asdict(obj)
        return obj

    @staticmethod
    def from_json(cls, json_data: Dict[str, Any]):
        return cls(**json_data)
