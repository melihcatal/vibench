from pydantic import BaseModel
from typing import Optional


class TokenResponse(BaseModel):
    access_token: str
    id_token: str
    refresh_token: Optional[str] = None
    expires_in: Optional[int] = None


class NormalizedProfile(BaseModel):
    sub: str
    name: Optional[str] = None
    given_name: Optional[str] = None
    family_name: Optional[str] = None
    email: Optional[str] = None
    picture: Optional[str] = None