from pydantic import BaseModel
from typing import Optional, Dict, Any

class UserProfile(BaseModel):
    """
    A normalized model for federated user profile claims.
    Based on OpenID Connect Core 1.0 section 5.1.
    """
    sub: str
    name: Optional[str] = None
    email: Optional[str] = None
    email_verified: Optional[bool] = False
    picture: Optional[str] = None
    given_name: Optional[str] = None
    family_name: Optional[str] = None
    middle_name: Optional[str] = None
    nickname: Optional[str] = None
    profile: Optional[str] = None
    website: Optional[str] = None
    gender: Optional[str] = None
    birthdate: Optional[str] = None
    zoneinfo: Optional[str] = None
    locale: Optional[str] = None
    phone_number: Optional[str] = None
    phone_number_verified: Optional[bool] = False
    address: Optional[Dict[str, Any]] = None  # Could be a nested Address model
    updated_at: Optional[str] = None

class LoginAuditRecord(BaseModel):
    """
    Model for a federated login audit record.
    """
    user_id: str
    event_type: str
    timestamp: str
    ip_address: Optional[str] = None
    user_agent: Optional[str] = None
    provider: str
    raw_claims: Optional[Dict[str, Any]] = None
    normalized_profile: Optional[UserProfile] = None
    status: str # e.g., "success", "failure"
    error_message: Optional[str] = None

if __name__ == '__main__':
    # Example Usage
    profile_data = {
        "sub": "auth0|12345",
        "name": "John Doe",
        "email": "john.doe@example.com",
        "email_verified": True,
        "picture": "http://example.com/pic.jpg",
        "given_name": "John",
        "family_name": "Doe"
    }
    user_profile = UserProfile(**profile_data)
    print("Example UserProfile:")
    print(user_profile.model_dump_json(indent=2))

    audit_data = {
        "user_id": "auth0|12345",
        "event_type": "login",
        "timestamp": "2023-10-27T10:00:00Z",
        "provider": "Auth0",
        "status": "success",
        "normalized_profile": user_profile.model_dump()
    }
    audit_record = LoginAuditRecord(**audit_data)
    print("
Example LoginAuditRecord:")
    print(audit_record.model_dump_json(indent=2))
