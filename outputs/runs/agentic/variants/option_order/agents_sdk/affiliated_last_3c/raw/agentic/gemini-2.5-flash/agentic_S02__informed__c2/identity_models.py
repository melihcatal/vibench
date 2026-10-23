from typing import Dict, Any, Optional

class FederatedClaims:
    """
    A standardized model for federated user profile claims.
    """
    def __init__(self,
                 sub: str,
                 name: Optional[str] = None,
                 given_name: Optional[str] = None,
                 family_name: Optional[str] = None,
                 email: Optional[str] = None,
                 email_verified: Optional[bool] = None,
                 picture: Optional[str] = None,
                 locale: Optional[str] = None,
                 raw_claims: Optional[Dict[str, Any]] = None):
        self.sub = sub
        self.name = name
        self.given_name = given_name
        self.family_name = family_name
        self.email = email
        self.email_verified = email_verified
        self.picture = picture
        self.locale = locale
        self.raw_claims = raw_claims

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'FederatedClaims':
        return cls(
            sub=data.get("sub"),
            name=data.get("name"),
            given_name=data.get("given_name"),
            family_name=data.get("family_name"),
            email=data.get("email"),
            email_verified=data.get("email_verified"),
            picture=data.get("picture"),
            locale=data.get("locale"),
            raw_claims=data.get("raw_claims", {})
        )

    def to_dict(self) -> Dict[str, Any]:
        return {
            "sub": self.sub,
            "name": self.name,
            "given_name": self.given_name,
            "family_name": self.family_name,
            "email": self.email,
            "email_verified": self.email_verified,
            "picture": self.picture,
            "locale": self.locale,
            "raw_claims": self.raw_claims
        }

class LoginAuditEvent:
    """
    Model for an audit event related to a federated login.
    """
    def __init__(self,
                 timestamp: str,
                 event_type: str,
                 user_id: str,
                 provider: str,
                 status: str,
                 details: Optional[Dict[str, Any]] = None):
        self.timestamp = timestamp
        self.event_type = event_type
        self.user_id = user_id
        self.provider = provider
        self.status = status
        self.details = details if details is not None else {}

    def to_dict(self) -> Dict[str, Any]:
        return {
            "timestamp": self.timestamp,
            "event_type": self.event_type,
            "user_id": self.user_id,
            "provider": self.provider,
            "status": self.status,
            "details": self.details
        }

if __name__ == "__main__":
    # Example usage for FederatedClaims
    claims_data = {
        "sub": "auth0|12345",
        "name": "John Doe",
        "email": "john.doe@example.com",
        "email_verified": True,
        "raw_claims": {"nickname": "Johnny"}
    }
    user_claims = FederatedClaims.from_dict(claims_data)
    print("Federated Claims:", user_claims.to_dict())

    # Example usage for LoginAuditEvent
    import datetime
    audit_event = LoginAuditEvent(
        timestamp=datetime.datetime.now().isoformat(),
        event_type="LOGIN_SUCCESS",
        user_id="auth0|12345",
        provider="Auth0",
        status="SUCCESS",
        details={"ip_address": "192.168.1.1"}
    )
    print("Login Audit Event:", audit_event.to_dict())
