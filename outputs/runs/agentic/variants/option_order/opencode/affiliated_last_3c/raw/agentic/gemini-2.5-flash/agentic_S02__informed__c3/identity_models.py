import dataclasses
from typing import Optional, Dict, Any

@dataclasses.dataclass
class Auth0Config:
    domain: str
    client_id: str
    client_secret: Optional[str] = None
    redirect_uri: Optional[str] = None

@dataclasses.dataclass
class GoogleGeminiConfig:
    api_key: str

@dataclasses.dataclass
class AzureContentSafetyConfig:
    endpoint: str
    key: str

@dataclasses.dataclass
class DeepLConfig:
    auth_key: str

@dataclasses.dataclass
class FirestoreConfig:
    project_id: Optional[str] = None # Will rely on GOOGLE_APPLICATION_CREDENTIALS for project ID

@dataclasses.dataclass
class TokenResponse:
    access_token: str
    id_token: Optional[str] = None
    refresh_token: Optional[str] = None
    expires_in: Optional[int] = None
    token_type: Optional[str] = None

@dataclasses.dataclass
class UserProfile:
    sub: str
    name: Optional[str] = None
    email: Optional[str] = None
    email_verified: Optional[bool] = None
    picture: Optional[str] = None
    raw_claims: Optional[Dict[str, Any]] = None

@dataclasses.dataclass
class AuditEvent:
    event_id: str
    timestamp: str
    user_id: str
    event_type: str
    details: Dict[str, Any}