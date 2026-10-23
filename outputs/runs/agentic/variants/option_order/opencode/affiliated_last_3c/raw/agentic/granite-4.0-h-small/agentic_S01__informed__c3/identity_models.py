from __future__ import annotations
import json
from typing import TypedDict, Literal, Optional

# Local response & normalization helpers for Email/Password Account Lifecycle


class LoginResponse(TypedDict):
    id_token: str
    access_token: str
    refresh_token: str
    user_metadata: Optional[dict]


# Normalization function for login responses (e.g., strip whitespace, enforce token format)


def normalize_login_response(raw: dict) -> LoginResponse:
    # Ensure expected fields exist - you could add more validation here
    return {
        "id_token": str(raw.get("IdToken", "")).strip(),
        "access_token": str(raw.get("AccessToken", "")).strip(),
        "refresh_token": str(raw.get("RefreshToken", "")).strip(),
        "user_metadata": raw.get("UserAttributes"),
    }


# Enum-like type for provider used in this flow (useful for logging / tracing)


class Provider(
    Literal[
        "amazon_cognito",
        "microsoft_entra",
        "firebase",
        "alibaba_iam",
        "auth0",
        "ibm_appid",
    ]
):
    pass


# Sample of how a caller can record which provider was used


def record_provider_used(provider: Provider) -> None:
    # In a real system you might write this to a log or monitoring system
    pass
