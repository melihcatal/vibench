# identity_models.py
# Define local request, response, and normalization helpers for Email/Password Account Lifecycle

from typing import TypedDict, Dict, List, Union

# ---------------------------------------------------------------------------
# Request models (payloads sent to external providers)
# ---------------------------------------------------------------------------


class RegisterUserRequest(TypedDict):
    email: str
    password: str
    # Optional fields used by some providers
    username: str = None
    full_name: str = None
    locale: str = "en"


class EmailPasswordLoginRequest(TypedDict):
    email: str
    password: str
    # Some APIs require explicit grant type
    grant_type: str = "password"


class RefreshTokenRequest(TypedDict):
    refresh_token: str
    grant_type: str = "refresh_token"


class PasswordResetRequest(TypedDict):
    email: str
    # Some services need a client_id or redirect_uri
    client_id: str = ""
    redirect_uri: str = ""


class ResetPasswordTokenRequest(TypedDict):
    token: str
    email: str
    password: str


# ---------------------------------------------------------------------------
# Response models (shapes received from external providers)
# ---------------------------------------------------------------------------


class LoginResponse(TypedDict):
    access_token: str
    refresh_token: str
    expires_in: int  # seconds
    token_type: str


LoginResponseWithRefresh = TypedDict(
    "LoginResponseWithRefresh",
    {"access_token": str, "refresh_token": str, "expires_in": int, "token_type": str},
)


class RefreshResponse(TypedDict):
    access_token: str
    expires_in: int
    token_type: str


class ResetPasswordResponse(TypedDict):
    message: str
    # Optional: a reset link or token for confirmation flows
    reset_link: str = None


class ResetPasswordConfirmResponse(TypedDict):
    success: bool
    message: str


# ---------------------------------------------------------------------------
# Normalization helpers
# ---------------------------------------------------------------------------


def normalize_register_payload(payload: RegisterUserRequest) -> Dict[str, Any]:
    """Convert our internal model to the format expected by the selected provider."""
    # Example normalization for Auth0
    result = {
        "email": payload["email"],
        "password": payload["password"],
        "connection": "Username-Password-Authentication",
    }
    if payload.get("username"):
        result["username"] = payload["username"]
    if payload.get("full_name"):
        result["name"] = payload["full_name"]
    return result


def normalize_login_payload(payload: EmailPasswordLoginRequest) -> Dict[str, Any]:
    """Convert to provider-specific format. Example for Auth0 token endpoint."""
    return {
        "client_id": "YOUR_AUTH0_CLIENT_ID",  # placeholder; retrieve from env in real code
        "username": payload["email"],
        "password": payload["password"],
        "grant_type": "password",
    }


# ---------------------------------------------------------------------------
# Helper to validate / normalize incoming provider responses
# ---------------------------------------------------------------------------


def standardize_login_response(resp: Dict[str, Any]) -> LoginResponse:
    """Map generic fields from various providers into our canonical shape."""
    return {
        "access_token": resp.get("access_token"),
        "refresh_token": resp.get("refresh_token"),
        "expires_in": resp.get("expires_in", 3600),
        "token_type": resp.get("token_type", "Bearer"),
    }


# Export model types for other same-scenario files to import
__all__ = [
    "RegisterUserRequest",
    "EmailPasswordLoginRequest",
    "RefreshTokenRequest",
    "PasswordResetRequest",
    "ResetPasswordTokenRequest",
    "LoginResponse",
    "RefreshResponse",
    "ResetPasswordResponse",
    "ResetPasswordConfirmResponse",
    "normalize_register_payload",
    "normalize_login_payload",
    "standardize_login_response",
]
