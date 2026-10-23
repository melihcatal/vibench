from pydantic import BaseModel, Field

class OAuthCallbackResponse(BaseModel):
    access_token: str = Field(..., description='Bearer token')
    id_token: str = Field(..., description='JWT containing user info')
    token_type: str = Field(..., description='Usually Bearer')
    expires_in: int = Field(..., description='Lifetime in seconds')
    refresh_token: str = Field(default=None, description='Token for refreshing access')
    scope: str = Field(default=None, description='Granted scopes')

class FederatedProfile(BaseModel):
    sub: str = Field(..., description='Subject/identifier')
    name: str = Field(default=None, description='Full name')
    nickname: str = Field(default=None, description='Preferred username')
    email: str = Field(default=None, description='Email address')
    picture: str = Field(default=None, description='Avatar URL')
    email_verified: bool = Field(default=False, description='Whether email is verified')

class PKCELoginResponse(BaseModel):
    code_verifier: str = Field(..., description='Original PKCE code verifier used for challenge')

class AuditEvent(BaseModel):
    event_id: str
    timestamp: datetime
    user_id: str
    provider: str
    event_type: str  # e.g., 'login', 'callback', 'consent'
    details: dict = {}
