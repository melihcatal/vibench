from typing import TypedDict, Dict, Any, Optional


class RegisterRequest(TypedDict):
    email: str
    password: str


class LoginRequest(TypedDict):
    email: str
    password: str


class RefreshRequest(TypedDict):
    refresh_token: str


class PasswordResetRequest(TypedDict):
    email: str


class AuthTokens(TypedDict):
    access_token: str
    id_token: str
    refresh_token: Optional[str]
    token_type: str
    expires_in: int


def parse_auth_result(result: Dict[str, Any]) -> AuthTokens:
    auth_result = result["AuthenticationResult"]
    return {
        "access_token": auth_result["AccessToken"],
        "id_token": auth_result["IdToken"],
        "refresh_token": auth_result.get("RefreshToken"),
        "token_type": auth_result["TokenType"],
        "expires_in": auth_result["ExpiresIn"],
    }
