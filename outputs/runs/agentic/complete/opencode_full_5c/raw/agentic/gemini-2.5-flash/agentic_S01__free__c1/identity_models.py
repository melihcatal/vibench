from pydantic import BaseModel, Field


class RegisterUserRequest(BaseModel):
    email: str = Field(..., description="User's email address")
    password: str = Field(..., description="User's password")


class RegisterUserResponse(BaseModel):
    uid: str = Field(..., description="Firebase User ID")
    email: str = Field(..., description="User's email address")


class EmailPasswordLoginRequest(BaseModel):
    email: str = Field(..., description="User's email address")
    password: str = Field(..., description="User's password")


class EmailPasswordLoginResponse(BaseModel):
    id_token: str = Field(..., alias="idToken", description="Firebase ID Token")
    refresh_token: str = Field(
        ..., alias="refreshToken", description="Firebase Refresh Token"
    )
    expires_in: str = Field(
        ..., alias="expiresIn", description="ID Token expiration duration"
    )


class RefreshSessionRequest(BaseModel):
    refresh_token: str = Field(
        ..., alias="refreshToken", description="Firebase Refresh Token"
    )


class RefreshSessionResponse(BaseModel):
    id_token: str = Field(..., alias="id_token", description="New Firebase ID Token")
    refresh_token: str = Field(
        ...,
        alias="refresh_token",
        description="New Firebase Refresh Token (if changed)",
    )
    expires_in: str = Field(
        ..., alias="expires_in", description="ID Token expiration duration"
    )


class PasswordResetRequest(BaseModel):
    email: str = Field(..., description="User's email address for password reset")


class PasswordResetResponse(BaseModel):
    message: str = Field(
        ..., description="Confirmation message for password reset email"
    )
