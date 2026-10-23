from pydantic import BaseModel, EmailStr, Field

# Local request/response models for Email/Password lifecycle


class SignupRequest(BaseModel):
    email: EmailStr = Field(..., description="User email address")
    password: str = Field(..., min_length=8, description="User password")
    first_name: str = Field("", description="Optional first name")
    last_name: str = Field("", description="Optional last name")


class SignupResponse(BaseModel):
    user_id: str
    confirmation_state: str


class LoginRequest(BaseModel):
    email: EmailStr = Field(..., description="User email address")
    password: str = Field(..., description="User password")


class LoginResponse(BaseModel):
    access_token: str
    id_token: str
    refresh_token: str


# Normalized response from password reset start
# Cognito's forgot_password returns ChallengeName and optional Session


class ResetStartResponse(BaseModel):
    challenge_name: str = Field(..., description="Challenge name (e.g., SMS_MFA)")
    session: str = Field("", description="Session token if required")


class ResetConfirmRequest(BaseModel):
    email: EmailStr = Field(..., description="User email address")
    reset_code: str = Field(..., description="Verification code sent by Cognito")
    new_password: str = Field(..., min_length=8, description="New password")


class ResetConfirmResponse(BaseModel):
    code_delivered: bool = True


# Helper for MFA SMS code submit


class MfaSubmitRequest(BaseModel):
    email: EmailStr = Field(..., description="User email address")
    reset_code: str = Field(..., description="Verification code")
    new_password: str = Field(..., min_length=8, description="New password after reset")


class MfaSubmitResponse(BaseModel):
    code_delivered: bool = True


# Generic error model (simple)
class ErrorResponse(BaseModel):
    error_code: str
    error_message: str
