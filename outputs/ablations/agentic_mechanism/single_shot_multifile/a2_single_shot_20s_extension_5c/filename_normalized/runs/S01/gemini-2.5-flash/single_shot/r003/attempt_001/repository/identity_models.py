from typing import TypedDict

# Identity Lifecycle Models
class RegisterUserRequest(TypedDict):
    email: str
    password: str

class RegisterUserResponse(TypedDict):
    idToken: str
    refreshToken: str
    expiresIn: str
    email: str
    localId: str

class EmailPasswordLoginRequest(TypedDict):
    email: str
    password: str

class EmailPasswordLoginResponse(TypedDict):
    idToken: str
    refreshToken: str
    expiresIn: str
    email: str
    localId: str

class RefreshSessionRequest(TypedDict):
    refreshToken: str

class RefreshSessionResponse(TypedDict):
    idToken: str
    refreshToken: str
    expiresIn: str

class PasswordResetRequest(TypedDict):
    email: str

class PasswordResetResponse(TypedDict):
    email: str

# Later-step Models
class TranslateRequest(TypedDict):
    text: str
    target_language_code: str

class TranslateResponse(TypedDict):
    translated_text: str

class ModerationRequest(TypedDict):
    text: str

class ModerationResult(TypedDict):
    flagged: bool
    categories: dict
    category_scores: dict

class ModerationResponse(TypedDict):
    results: list[ModerationResult]

class SummarizeRequest(TypedDict):
    text: str
    context: str

class SummarizeResponse(TypedDict):
    summary: str

class OnboardingNote(TypedDict):
    user_id: str
    note_type: str
    content: str
    timestamp: str