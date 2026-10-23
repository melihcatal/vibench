from pydantic import BaseModel, EmailStr, Field

class UserCreateRequest(BaseModel):
    email: EmailStr
    password: str
    first_name: str = Field(default_factory=str)
    last_name: str = Field(default_factory=str)

class UserCreateResponse(BaseModel):
    user_id: str
    email: EmailStr
    created_at: str
    user_metadata: dict

class TokenResponse(BaseModel):
    access_token: str
    id_token: str
    refresh_token: str
    token_type: str = "Bearer"
    expires_in: int

class RefreshTokenRequest(BaseModel):
    grant_type: str = "refresh_token"
    client_id: str
    client_secret: str
    refresh_token: str
    audience: str

class RefreshTokenResponse(BaseModel):
    access_token: str
    id_token: str
    refresh_token: str
    token_type: str = "Bearer"
    expires_in: int

# Normalizer helpers (optional)\nfrom typing import Any\n\ndef normalize_token_response(raw: dict[str, Any]) -> TokenResponse:\n    return TokenResponse.parse_obj(raw)\n\ndef normalize_user_create_response(raw: dict[str, Any]) -> UserCreateResponse:\n    return UserCreateResponse.parse_obj(raw)\n\ndef normalize_refresh_response(raw: dict[str, Any]) -> RefreshTokenResponse:\n    return RefreshTokenResponse.parse_obj(raw)
