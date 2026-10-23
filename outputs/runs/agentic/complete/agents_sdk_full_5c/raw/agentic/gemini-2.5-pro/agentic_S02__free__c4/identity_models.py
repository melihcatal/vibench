from pydantic import BaseModel, EmailStr
from typing import Optional

class UserProfile(BaseModel):
    """
    A Pydantic model to represent and validate normalized user claims
    from an identity provider.
    """
    sub: str
    name: Optional[str] = None
    email: Optional[EmailStr] = None
    email_verified: Optional[bool] = False
    preferred_username: Optional[str] = None
    zoneinfo: Optional[str] = None
    locale: Optional[str] = None
    updated_at: Optional[int] = None
