# identity_models.py

from pydantic import BaseModel, EmailStr
from datetime import datetime

# Request models


class CreateUserRequest(BaseModel):
    email: EmailStr
    password: str
    connection: str = "Username-Password-Authentication"


# Response models


class AuthResponse(BaseModel):
    access_token: str
    token_type: str
    expires_in: int
    refresh_token: str


class UserResponse(BaseModel):
    user_id: str
    email: EmailStr
    email_verified: bool
    created_at: datetime
    updated_at: datetime


# Normalization helpers


def normalize_user_response(data: dict) -> UserResponse:
    return UserResponse(
        user_id=data.get("user_id"),
        email=data.get("email"),
        email_verified=data.get("email_verified"),
        created_at=datetime.fromisoformat(data.get("created_at")),
        updated_at=datetime.fromisoformat(data.get("updated_at")),
    )


def normalize_auth_response(data: dict) -> AuthResponse:
    return AuthResponse(
        access_token=data.get("access_token"),
        token_type=data.get("token_type"),
        expires_in=data.get("expires_in"),
        refresh_token=data.get("refresh_token"),
    )


# Utility helpers


def serialize_request(req: CreateUserRequest) -> dict:
    return {
        "email": req.email,
        "password": req.password,
        "connection": req.connection,
        "email_verified": False,  # set during creation
    }
