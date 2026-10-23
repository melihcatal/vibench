# identity_models.py
# Local request, response, and normalization helpers for Email/Password Account Lifecycle

import json
from typing import TypedDict, List, Optional

# ------------------------ Request Models --------------------------


class CreateUserRequest(TypedDict):
    email: str
    password: str
    display_name: Optional[str] = None
    extra: Optional[dict] = None


class LoginRequest(TypedDict):
    email: str
    password: str


class RefreshRequest(TypedDict):
    refresh_token: str


class ResetPasswordRequest(TypedDict):
    email: str
    new_password: str
    request_id: Optional[str] = None


# ------------------------ Response Models --------------------------


class CreateUserResponse(TypedDict):
    user_id: str
    email: str
    created_at: int


class LoginResponse(TypedDict):
    access_token: str
    refresh_token: str
    expires_in: int
    token_type: str = "Bearer"


class RefreshResponse(TypedDict):
    access_token: str
    expires_in: int
    token_type: str = "Bearer"


class ResetPasswordResponse(TypedDict):
    message: str


# ------------------------ Normalization Helpers --------------------------


def normalize_create_user_payload(payload: CreateUserRequest) -> dict:
    """Normalize payload to provider-specific format (e.g., Firebase)."""
    data = {
        "email": payload["email"],
        "password": payload["password"],
        "displayName": payload.get("display_name"),
    }
    extra = payload.get("extra", {})
    data.update(extra)
    return data


def normalize_login_payload(payload: LoginRequest) -> dict:
    return {
        "email": payload["email"],
        "password": payload["password"],
    }


def normalize_refresh_payload(payload: RefreshRequest) -> dict:
    return {"refresh_token": payload["refresh_token"]}


def normalize_reset_payload(payload: ResetPasswordRequest) -> dict:
    return {
        "newPassword": payload["new_password"],
        "email": payload["email"],
        "requestId": payload.get("request_id"),
    }


# ------------------------ Serialization --------------------------


def serialize_response(resp: dict) -> str:
    return json.dumps(resp, indent=2)


# Example usage (not executed in this file)
# payload = CreateUserRequest(email="user@example.com", password="Pass123!")
# provider_data = normalize_create_user_payload(payload)
