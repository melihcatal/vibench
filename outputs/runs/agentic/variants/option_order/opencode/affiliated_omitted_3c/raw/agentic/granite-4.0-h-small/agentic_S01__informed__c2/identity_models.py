# identity_models.py
# Define local request, response, and normalization helpers for Email/Password Account Lifecycle

from pydantic import BaseModel, EmailStr, validator
from typing import Optional, Dict

# ------------------- Input Models -------------------


class RegisterUserRequest(BaseModel):
    email: EmailStr
    password: str
    # optional onboarding notes
    notes: Optional[str] = None

    @validator("password")
    def validate_password(cls, v: str) -> str:
        # simple password policy: min 8 chars, at least one digit and one special char
        if len(v) < 8:
            raise ValueError("Password must be at least 8 characters")
        if not any(char.isdigit() for char in v):
            raise ValueError("Password must contain at least one digit")
        if not any(not char.isalnum() for char in v):
            raise ValueError("Password must contain at least one special character")
        return v


class EmailPasswordLoginRequest(BaseModel):
    email: EmailStr
    password: str


class RefreshTokenRequest(BaseModel):
    refresh_token: str


# ------------------- Output Models -------------------


class AuthSuccess(BaseModel):
    access_token: str
    expires_in: int  # seconds
    token_type: str = "Bearer"
    refresh_token: Optional[str] = None

    def to_dict(self) -> Dict[str, Any]:
        return self.dict()


class ResetPasswordRequest(BaseModel):
    email: EmailStr


class ResetPasswordConfirmationRequest(BaseModel):
    email: EmailStr
    token: str
    new_password: str


# ------------------- Normalization Helpers -------------------


def normalize_user_profile(profile: Dict[str, Any]) -> Dict[str, Any]:
    """Convert provider-specific profile into a unified internal format.

    Example shape:
    {
        "user_id": str,
        "email": str,
        "locale": str,
        "status": str,  # e.g., "active", "pending"
        "created_at": str,  # ISO datetime
    }
    """
    # Placeholder implementation – replace with provider-specific mapping logic
    return {
        "user_id": profile.get("sub") or profile.get("id"),
        "email": profile.get("email"),
        "locale": profile.get("locale") or "en-US",
        "status": profile.get("status") or "active",
        "created_at": profile.get("created_at") or None,
    }


# End of file
