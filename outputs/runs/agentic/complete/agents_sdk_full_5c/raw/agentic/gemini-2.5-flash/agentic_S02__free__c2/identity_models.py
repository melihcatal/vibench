from typing import Optional, Dict, Any
from datetime import datetime

class UserProfileClaims:
    """Standardized structure for federated user profile claims."""
    def __init__self,
        provider: str,
        sub: str,
        email: Optional[str] = None,
        email_verified: bool = False,
        name: Optional[str] = None,
        given_name: Optional[str] = None,
        family_name: Optional[str] = None,
        picture: Optional[str] = None,
        locale: Optional[str] = None,
        raw_claims: Optional[Dict[str, Any]] = None,
    ):
        self.provider = provider
        self.sub = sub
        self.email = email
        self.email_verified = email_verified
        self.name = name
        self.given_name = given_name
        self.family_name = family_name
        self.picture = picture
        self.locale = locale
        self.raw_claims = raw_claims if raw_claims is not None else {}

    def to_dict(self) -> Dict[str, Any]:
        return {
            "provider": self.provider,
            "sub": self.sub,
            "email": self.email,
            "email_verified": self.email_verified,
            "name": self.name,
            "given_name": self.given_name,
            "family_name": self.family_name,
            "picture": self.picture,
            "locale": self.locale,
            "raw_claims": self.raw_claims,
        }

class LoginAuditEvent:
    """Structure for a federated login audit event."""
    def __init__(
        self,
        timestamp: datetime,
        user_id: str,
        provider: str,
        event_type: str, # e.g., 'login_success', 'login_failure', 'token_refresh'
        ip_address: Optional[str] = None,
        user_agent: Optional[str] = None,
        session_id: Optional[str] = None,
        details: Optional[Dict[str, Any]] = None,
        notes: Optional[str] = None,
    ):
        self.timestamp = timestamp
        self.user_id = user_id
        self.provider = provider
        self.event_type = event_type
        self.ip_address = ip_address
        self.user_agent = user_agent
        self.session_id = session_id
        self.details = details if details is not None else {}
        self.notes = notes

    def to_dict(self) -> Dict[str, Any]:
        return {
            "timestamp": self.timestamp.isoformat(),
            "user_id": self.user_id,
            "provider": self.provider,
            "event_type": self.event_type,
            "ip_address": self.ip_address,
            "user_agent": self.user_agent,
            "session_id": self.session_id,
            "details": self.details,
            "notes": self.notes,
        }

if __name__ == "__main__":
    # Example usage for UserProfileClaims
    sample_profile_data = {
        "sub": "12345",
        "email": "test@example.com",
        "name": "Test User",
        "provider": "google"
    }
    profile = UserProfileClaims(**sample_profile_data)
    print("Sample User Profile Claims:", profile.to_dict())

    # Example usage for LoginAuditEvent
    event = LoginAuditEvent(
        timestamp=datetime.now(),
        user_id="user-abc-123",
        provider="okta",
        event_type="login_success",
        ip_address="192.168.1.1",
        notes="User successfully logged in via Okta PKCE flow."
    )
    print("\nSample Login Audit Event:", event.to_dict())
