from typing import TypedDict, Literal, Dict

# HELPER: Typed request/response models and utility helpers


class RegisterRequest(TypedDict):
    email: str
    password: str


class RegisterResponse(TypedDict):
    user_id: str
    status: Literal["created"]


class LoginRequest(TypedDict):
    email: str
    password: str


class LoginResponse(TypedDict):
    access_token: str
    refresh_token: str
    token_type: Literal["bearer"]


class RefreshRequest(TypedDict):
    refresh_token: str


class RefreshResponse(TypedDict):
    access_token: str
    token_type: Literal["bearer"]


class ResetRequest(TypedDict):
    email: str


class ResetResponse(TypedDict):
    reset_id: str
    instructions: str  # e.g., \"Check your inbox for a reset link.\"


# Normalization utilities


def normalize_register_response(data: Dict[str, Any]) -> RegisterResponse:
    """Convert provider-specific response into the canonical RegisterResponse shape."""
    # Example mapping - replace with provider-specific logic
    return RegisterResponse(
        user_id=data.get("user_id") or str(data.get("id")), status="created"
    )


def normalize_login_response(data: Dict[str, Any]) -> LoginResponse:
    return LoginResponse(
        access_token=data["access_token"],
        refresh_token=data["refresh_token"],
        token_type=data.get("token_type", "bearer"),
    )


def normalize_refresh_response(data: Dict[str, Any]) -> RefreshResponse:
    return RefreshResponse(
        access_token=data["access_token"], token_type=data.get("token_type", "bearer")
    )


def normalize_reset_response(data: Dict[str, Any]) -> ResetResponse:
    return ResetResponse(
        reset_id=data.get("reset_id") or data.get("id"),
        instructions=data.get("instructions") or "Check the email for reset details.",
    )
