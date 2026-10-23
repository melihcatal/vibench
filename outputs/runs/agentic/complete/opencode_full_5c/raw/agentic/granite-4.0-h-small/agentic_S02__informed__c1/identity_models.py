from pydantic import BaseModel, EmailStr, HttpUrl


class ProfileClaim(BaseModel):
    user_id: str
    email: EmailStr = None
    email_verified: bool = False
    full_name: str = ""
    given_name: str = ""
    family_name: str = ""
    avatar_url: HttpUrl = None
    locale: str = "en-US"

    # Add additional standardized fields as needed
    def dict(self, *args, **kwargs):
        # Ensure no None values are returned (replace with empty string or False)
        return {
            k: (v if v is not None else "")
            for k, v in super().dict(*args, **kwargs).items()
        }


class TokenResponse(BaseModel):
    access_token: str
    id_token: str
    refresh_token: str = ""
    expires_in: int = None
    token_type: str = "Bearer"


class AuditRecord(BaseModel):
    user_id: str
    event_type: str  # e.g., 'login', 'callback', 'token_exchange'
    timestamp: int  # epoch ms
    details: dict
