from typing import Optional

class RegisterUserRequest:
    def __init__(self, email: str, password: str):
        self.email = email
        self.password = password

class RegisterUserResponse:
    def __init__(self, user_id: str, message: str):
        self.user_id = user_id
        self.message = message

class LoginRequest:
    def __init__(self, email: str, password: str):
        self.email = email
        self.password = password

class LoginResponse:
    def __init__(self, access_token: str, refresh_token: str, id_token: str, expires_in: int):
        self.access_token = access_token
        self.refresh_token = refresh_token
        self.id_token = id_token
        self.expires_in = expires_in

class RefreshSessionRequest:
    def __init__(self, refresh_token: str):
        self.refresh_token = refresh_token

class RefreshSessionResponse:
    def __init__(self, access_token: str, id_token: str, expires_in: int):
        self.access_token = access_token
        self.id_token = id_token
        self.expires_in = expires_in

class PasswordResetRequest:
    def __init__(self, email: str):
        self.email = email

class PasswordResetResponse:
    def __init__(self, message: str):
        self.message = message

class TranslateRequest:
    def __init__(self, text: str, source_language_code: str, target_language_code: str):
        self.text = text
        self.source_language_code = source_language_code
        self.target_language_code = target_language_code

class TranslateResponse:
    def __init__(self, translated_text: str):
        self.translated_text = translated_text

class ModerateProfileRequest:
    def __init__(self, profile_text: str):
        self.profile_text = profile_text

class ModerateProfileResponse:
    def __init__(self, is_moderated: bool, moderation_labels: list):
        self.is_moderated = is_moderated
        self.moderation_labels = moderation_labels

class OnboardingSummaryRequest:
    def __init__(self, onboarding_data: str):
        self.onboarding_data = onboarding_data

class OnboardingSummaryResponse:
    def __init__(self, summary: str):
        self.summary = summary

class ProfileNoteStoreRequest:
    def __init__(self, user_id: str, note_content: str, metadata: Optional[dict] = None):
        self.user_id = user_id
        self.note_content = note_content
        self.metadata = metadata

class ProfileNoteStoreResponse:
    def __init__(self, success: bool, note_id: Optional[str] = None, message: Optional[str] = None):
        self.success = success
        self.note_id = note_id
        self.message = message
