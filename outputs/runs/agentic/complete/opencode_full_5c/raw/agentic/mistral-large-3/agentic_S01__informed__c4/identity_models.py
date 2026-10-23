from typing import Dict, Any, Optional
from pydantic import BaseModel, EmailStr


class RegisterRequest(BaseModel):
    email: EmailStr
    password: str
    connection: str = "Username-Password-Authentication"
    user_metadata: Optional[Dict[str, Any]] = None


class RegisterResponse(BaseModel):
    user_id: str
    email: EmailStr
    email_verified: bool
    created_at: str


class LoginRequest(BaseModel):
    email: EmailStr
    password: str
    client_id: str
    grant_type: str = "password"


class LoginResponse(BaseModel):
    access_token: str
    refresh_token: str
    id_token: str
    expires_in: int


class RefreshRequest(BaseModel):
    refresh_token: str
    client_id: str
    grant_type: str = "refresh_token"


class RefreshResponse(BaseModel):
    access_token: str
    expires_in: int
    id_token: str


class PasswordResetRequest(BaseModel):
    email: EmailStr
    client_id: str


class PasswordResetResponse(BaseModel):
    status: str


def normalize_register_request(request: RegisterRequest) -> Dict[str, Any]:
    return {
        "email": request.email,
        "password": request.password,
        "connection": request.connection,
        "user_metadata": request.user_metadata or {},
    }


def normalize_register_response(response: Dict[str, Any]) -> RegisterResponse:
    return RegisterResponse(
        user_id=response["user_id"],
        email=response["email"],
        email_verified=response["email_verified"],
        created_at=response["created_at"],
    )
