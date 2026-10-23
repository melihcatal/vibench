from typing import Optional, Dict, Any
from dataclasses import dataclass
from datetime import datetime


@dataclass
class UserRegistrationRequest:
    """Request model for user registration."""

    email: str
    password: str
    display_name: Optional[str] = None
    metadata: Optional[Dict[str, Any]] = None


@dataclass
class UserRegistrationResponse:
    """Response model for user registration."""

    user_id: str
    email: str
    session_token: Optional[str] = None
    refresh_token: Optional[str] = None
    display_name: Optional[str] = None
    created_at: Optional[datetime] = None


@dataclass
class LoginRequest:
    """Request model for login."""

    email: str
    password: str


@dataclass
class LoginResponse:
    """Response model for login."""

    user_id: str
    email: str
    access_token: str
    refresh_token: str
    expires_at: Optional[int] = None
    display_name: Optional[str] = None
    profile_data: Optional[Dict[str, Any]] = None


@dataclass
class RefreshRequest:
    """Request model for session refresh."""

    refresh_token: str


@dataclass
class RefreshResponse:
    """Response model for session refresh."""

    user_id: str
    email: str
    access_token: str
    refresh_token: str
    expires_at: Optional[int] = None
    token_type: str = "bearer"


@dataclass
class PasswordResetRequest:
    """Request model for password reset."""

    email: str
    redirect_url: Optional[str] = None


@dataclass
class PasswordResetResponse:
    """Response model for password reset."""

    email: str
    reset_sent: bool
    message: str
    redirect_url: Optional[str] = None


@dataclass
class TranslationRequest:
    """Request model for translation."""

    text: str
    target_lang: str
    source_lang: Optional[str] = None


@dataclass
class TranslationResponse:
    """Response model for translation."""

    translated_text: str
    source_lang: str
    target_lang: str
    detected_source_lang: Optional[str] = None


@dataclass
class ModerationRequest:
    """Request model for content moderation."""

    text: str
    content_type: str = "profile"


@dataclass
class ModerationResponse:
    """Response model for content moderation."""

    is_approved: bool
    flagged_categories: Optional[Dict[str, float]] = None
    moderation_score: Optional[float] = None
    sanitized_text: Optional[str] = None


@dataclass
class SummaryRequest:
    """Request model for summarization."""

    text: str
    max_length: Optional[int] = 200


@dataclass
class SummaryResponse:
    """Response model for summarization."""

    summary: str
    original_length: int
    summary_length: int
    key_points: Optional[list[str]] = None


@dataclass
class ProfileNote:
    """Model for profile notes."""

    user_id: str
    note_id: str
    content: str
    note_type: str
    created_at: datetime
    updated_at: Optional[datetime] = None
    metadata: Optional[Dict[str, Any]] = None


def normalize_auth_response(auth_data: Dict[str, Any]) -> Dict[str, Any]:
    """Normalize authentication response from various providers."""
    normalized = {
        "user_id": auth_data.get("id")
        or auth_data.get("user_id")
        or auth_data.get("sub"),
        "email": auth_data.get("email"),
        "access_token": auth_data.get("access_token") or auth_data.get("session_token"),
        "refresh_token": auth_data.get("refresh_token"),
        "expires_at": auth_data.get("expires_at") or auth_data.get("expires_in"),
        "token_type": auth_data.get("token_type", "bearer"),
    }

    # Remove None values
    return {k: v for k, v in normalized.items() if v is not None}


def create_error_response(error: Exception, context: str = "") -> Dict[str, Any]:
    """Create standardized error response."""
    return {
        "success": False,
        "error": str(error),
        "error_type": type(error).__name__,
        "context": context,
        "timestamp": datetime.now().isoformat(),
    }
