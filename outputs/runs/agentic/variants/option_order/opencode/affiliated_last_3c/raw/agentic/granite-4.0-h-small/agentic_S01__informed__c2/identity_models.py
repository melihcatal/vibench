# [HELPER] identity_models.py
# Define request, response, and normalization helpers for Email/Password Account Lifecycle

from typing import TypedDict, Optional

# Payload models -----------------------------------------------------------


class RegisterUserRequest(TypedDict):
    email: str
    password: str
    connection: Optional[str]  # defaults to Username-Password-Authentication


class LoginRequest(TypedDict):
    email: str
    password: str


class RefreshTokenRequest(TypedDict):
    refresh_token: str


class PasswordResetRequest(TypedDict):
    email: str
    connection: Optional[str]


# Normalization helpers ----------------------------------------------------


def normalize_register_payload(payload: dict) -> RegisterUserRequest:
    """Ensure required fields exist and set defaults."""
    payload = dict(payload)
    payload.setdefault("connection", "Username-Password-Authentication")
    return payload


# End of models module
