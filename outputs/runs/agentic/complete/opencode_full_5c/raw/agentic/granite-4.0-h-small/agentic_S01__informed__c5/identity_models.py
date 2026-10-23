# identity_models.py
# Define local request, response, and normalization helpers for Email/Password Account Lifecycle

import json
import datetime
from typing import TypedDict, Optional


class LoginRequest(TypedDict):
    email: str
    password: str


class LoginResponse(TypedDict):
    access_token: str
    refresh_token: Optional[str]
    expires_in: int  # seconds
    token_type: str


class RefreshRequest(TypedDict):
    refresh_token: str


class RefreshResponse(TypedDict):
    access_token: str
    expires_in: int


class PasswordResetRequest(TypedDict):
    email: str


class PasswordResetResponse(TypedDict):
    reset_id: str
    expires_in: int


class ProfileData(TypedDict):
    user_id: str
    email: str
    locale: str
    full_name: Optional[str]
    created_at: datetime.datetime


def normalize_user_id(user_id: str) -> str:
    """Normalize a Firebase or AppID user identifier to a canonical UUIDv4 string."""
    # Example normalization: strip non-uuid characters, ensure lowercase
    return user_id.strip().lower()


def serialize_timestamp(dt: datetime.datetime) -> str:
    """Serialize a datetime to ISO 8601 string for storage."""
    return dt.isoformat() + "Z"


def deserialize_timestamp(ts_str: str) -> datetime.datetime:
    """Deserialize ISO 8601 string to datetime object."""
    return datetime.datetime.fromisoformat(ts_str.replace("Z", "+00:00"))


def parse_json_response(resp):
    """Parse JSON response and raise if not successful."""
    try:
        data = resp.json()
    except json.JSONDecodeError:
        raise ValueError("Invalid JSON response")
    if resp.status_code >= 400:
        raise RuntimeError(
            f"API error: {data.get('error')}, {data.get('error_description')}"
        )
    return data
