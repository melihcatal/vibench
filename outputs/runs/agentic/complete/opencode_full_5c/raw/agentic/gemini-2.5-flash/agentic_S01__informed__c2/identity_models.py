import dataclasses
from typing import Optional


@dataclasses.dataclass
class RegisterUserRequest:
    email: str
    password: str
    connection: str = "Username-Password-Authentication"


@dataclasses.dataclass
class RegisterUserResponse:
    user_id: str
    email: str
    email_verified: bool


@dataclasses.dataclass
class LoginUserRequest:
    email: str
    password: str
    realm: str = "Username-Password-Authentication"
    scope: str = "openid profile email offline_access"
    audience: str = "YOUR_AUTH0_AUDIENCE"  # Replace with your actual audience


@dataclasses.dataclass
class LoginUserResponse:
    access_token: str
    id_token: str
    refresh_token: Optional[str] = None
    expires_in: int
    token_type: str


@dataclasses.dataclass
class RefreshTokenRequest:
    refresh_token: str
    scope: str = "openid profile email offline_access"


@dataclasses.dataclass
class RefreshTokenResponse:
    access_token: str
    id_token: str
    expires_in: int
    token_type: str


@dataclasses.dataclass
class PasswordResetRequest:
    email: str
    connection: str = "Username-Password-Authentication"


@dataclasses.dataclass
class TranslateTextRequest:
    text: str
    target_language: str


@dataclasses.dataclass
class TranslateTextResponse:
    translated_text: str


@dataclasses.dataclass
class ModerateProfileRequest:
    text: str


@dataclasses.dataclass
class ModerationResult:
    category: str
    severity: int


@dataclasses.dataclass
class ModerateProfileResponse:
    is_safe: bool
    results: list[ModerationResult]


@dataclasses.dataclass
class OnboardingSummaryRequest:
    onboarding_data: dict


@dataclasses.dataclass
class OnboardingSummaryResponse:
    summary: str


@dataclasses.dataclass
class ProfileNote:
    user_id: str
    timestamp: str
    note: str
    metadata: dict


@dataclasses.dataclass
class StoreProfileNoteRequest:
    note: ProfileNote


@dataclasses.dataclass
class StoreProfileNoteResponse:
    document_id: str
