import dataclasses

# Local helper: identity_models.py
# Defines request/response structures and normalization helpers for Email/Password Account Lifecycle


@dataclasses.dataclass
class CreateUserRequest:
    email: str
    password: str
    # optional fields (e.g., first_name, last_name) can be added here


@dataclass
class CreateUserResponse:
    user_id: str
    email: str
    created_at: str


@dataclass
class TokenResponse:
    access_token: str
    refresh_token: str
    token_type: str
    expires_in: int


@dataclass
class PasswordResetRequest:
    email: str


@dataclass
class PasswordResetResponse:
    request_id: str
    message: str


# Normalization helpers


def normalize_user_input(data: dict) -> CreateUserRequest:
    """Extract required fields from a generic dict and validate."""
    return CreateUserRequest(email=data.get("email"), password=data.get("password"))


def serialize_token_response(resp: TokenResponse) -> dict:
    """Serialize model to JSON-friendly dict."""
    return {
        "access_token": resp.access_token,
        "refresh_token": resp.refresh_token,
        "token_type": resp.token_type,
        "expires_in": resp.expires_in,
    }
