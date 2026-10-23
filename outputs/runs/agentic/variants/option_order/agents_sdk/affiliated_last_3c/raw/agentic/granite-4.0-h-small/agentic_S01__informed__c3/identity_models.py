from typing import TypedDict, Literal

class UserRegisterResponse(TypedDict):
    UserSub: str
    UserCreated: Literal['TRUE']

class AuthTokens(TypedDict):
    AccessToken: str
    IdToken: str
    RefreshToken: str

class ResetPasswordResponse(TypedDict):
    code_delivery_details: dict
