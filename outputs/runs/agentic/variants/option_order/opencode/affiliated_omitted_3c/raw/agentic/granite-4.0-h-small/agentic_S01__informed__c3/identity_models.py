from typing import TypedDict, List


class EmailAttribute(TypedDict):
    Name: str
    Value: str


class UserAttribute(TypedDict):
    Name: str
    Value: str


# Normalized representation of a user record returned by identity services
class NormalizedUser(TypedDict):
    Username: str
    Email: str
    Sub: str
    Attributes: List[UserAttribute]


# Payload for password reset requests
class ResetPasswordRequest(TypedDict):
    Username: str
    Code: str
    NewPassword: str


# Optional response fields after a successful sign-up or login
class TokenResponse(TypedDict):
    IDToken: str
    AccessToken: str
    RefreshToken: str
    ExpiresIn: int
    TokenType: str


# DeepL translation result model
class DeepLTranslation(TypedDict):
    text: str
    detected_source_language: str
