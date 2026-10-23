from pydantic import BaseModel, EmailStr, ValidationError

# -------------------------------------------------
# Local request / response models for Email/Password flow
# -------------------------------------------------

class CreateUserRequest(BaseModel):
    email: EmailStr
    password: str

class CreateUserResponse(BaseModel):
    user_sub: str

class LoginRequest(BaseModel):
    email: EmailStr
    password: str

class LoginResponse(BaseModel):
    id_token: str
    refresh_token: str

class RefreshTokenRequest(BaseModel):
    refresh_token: str

class RefreshTokenResponse(BaseModel):
    id_token: str
    refresh_token: str

class ResetPasswordRequest(BaseModel):
    email: EmailStr

class ResetPasswordResponse(BaseModel):
    code_delivery_details: dict  # cloud‑specific delivery info

# Helper to validate and normalize inputs
def validate_create(payload):
    try:
        return CreateUserRequest(**payload).dict()
    except ValidationError as exc:
        raise ValueError(f"Invalid create payload: {exc}")

def validate_login(payload):
    try:
        return LoginRequest(**payload).dict()
    except ValidationError as exc:
        raise ValueError(f"Invalid login payload: {exc}")
