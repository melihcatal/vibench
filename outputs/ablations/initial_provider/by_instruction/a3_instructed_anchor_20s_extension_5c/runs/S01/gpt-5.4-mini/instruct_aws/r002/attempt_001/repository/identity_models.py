from dataclasses import dataclass
from typing import Any, Dict, Optional


def normalize_email(email: str) -> str:
    return email.strip().lower()


def normalize_locale(locale: Optional[str]) -> str:
    return (locale or "en").strip().replace("_", "-") or "en"


@dataclass
class EmailPasswordRequest:
    email: str
    password: str
    locale: str = "en"


@dataclass
class AuthTokens:
    access_token: str
    refresh_token: str
    id_token: Optional[str] = None
    expires_in: Optional[int] = None
    token_type: Optional[str] = None


@dataclass
class PasswordResetRequest:
    email: str


@dataclass
class TranslationRequest:
    text: str
    locale: str


@dataclass
class ModerationRequest:
    text: str


@dataclass
class OnboardingSummaryRequest:
    user_id: str
    locale: str


def tokens_from_cognito_response(payload: Dict[str, Any]) -> AuthTokens:
    return AuthTokens(
        access_token=payload.get("AccessToken", ""),
        refresh_token=payload.get("RefreshToken", ""),
        id_token=payload.get("IdToken"),
        expires_in=payload.get("ExpiresIn"),
        token_type=payload.get("TokenType"),
    )
