from dataclasses import dataclass


@dataclass
class UserRegistration:
    email: str
    password: str


@dataclass
class UserCredentials:
    email: str
    password: str


@dataclass
class AuthTokens:
    id_token: str
    refresh_token: str
    expires_in: int


@dataclass
class PasswordResetRequest:
    email: str


@dataclass
class OnboardingState:
    user_id: str
    profile_text: str
    user_locale: str
    moderation_result: dict
    translation_result: dict


@dataclass
class ProfileNote:
    user_id: str
    note_id: str
    content: str
    summary: str
