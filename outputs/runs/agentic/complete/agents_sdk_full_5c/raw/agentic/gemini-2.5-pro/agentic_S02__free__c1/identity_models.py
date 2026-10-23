from pydantic import BaseModel, Field
from typing import Optional, Dict, Any


class TokenData(BaseModel):
    access_token: str
    token_type: str
    expires_in: int
    scope: str
    id_token: Optional[str] = None
    refresh_token: Optional[str] = None


class NormalizedUser(BaseModel):
    id: str
    name: Optional[str] = None
    email: Optional[str] = None
    username: Optional[str] = None
    picture: Optional[str] = None
    raw_claims: Dict[str, Any] = Field(default_factory=dict)
