from pydantic import BaseModel, EmailStr, Field

class RegisterRequest(BaseModel):
    ClientId: str = Field(..., description="Cognito User Pool client ID")
    Username: str = Field(..., description="Email address to be registered")
    Password: str = Field(..., description="Plain text password")
    UserAttributes: list[dict] = Field(
        default_factory=list,
        description="Additional attributes (e.g., email verified, locale)",
    )

class RegisterResponse(BaseModel):
    UserSub: str = Field(..., description="Unique user identifier")
    UserCreated: bool = Field(..., description="Whether a new user record was created")
    CodeDeliveryDetails: dict = Field(default=None, description="MFA/verification details if any")

class LoginRequest(BaseModel):
    ClientId: str = Field(..., description="Cognito User Pool client ID")
    AuthFlow: str = Field(..., description="Authentication flow (e.g., USER_PASSWORD_AUTH)")
    AuthParameters: dict = Field(..., description="Credentials: USERNAME and PASSWORD")
    UserPoolId: str = Field(..., description="Cognito User Pool ID")

class LoginResponse(BaseModel):
    AuthenticationResult: dict = Field(
        ...,
        description="Tokens and token metadata returned by Cognito",
    )

class TokenRefreshRequest(BaseModel):
    ClientId: str = Field(..., description="Cognito User Pool client ID")
    RefreshToken: str = Field(..., description="Existing refresh token")
    AuthFlow: str = Field(..., description="REFRESH_TOKEN_AUTH")
    AuthParameters: dict = Field(..., description="REFRESH_TOKEN key/value pair")
    UserPoolId: str = Field(..., description="Cognito User Pool ID")

class TokenRefreshResponse(BaseModel):
    AuthenticationResult: dict = Field(
        ...,
        description="New tokens (id_token, access_token, refresh_token) and expiry",
    )

class PasswordResetRequest(BaseModel):
    ClientId: str = Field(..., description="Cognito User Pool client ID")
    Username: str = Field(..., description="Email address requesting reset")

class PasswordResetResponse(BaseModel):
    CodeDeliveryDetails: dict = Field(
        ...,
        description="Details of the reset code delivery (e.g., email subject, destination)",
    )
