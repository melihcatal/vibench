from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional, Dict, Any, List

@dataclass
class UserProfileClaims:
    """
    Standardized user profile claims based on OIDC Core 1.0.
    """
    sub: str # Subject - Identifier for the End-User at the Issuer.
    name: Optional[str] = None # End-User's full name.
    given_name: Optional[str] = None # Given name(s) or first name(s) of the End-User.
    family_name: Optional[str] = None # Surname(s) or last name(s) of the End-User.
    middle_name: Optional[str] = None # Middle name(s) of the End-User.
    nickname: Optional[str] = None # Casual name of the End-User.
    preferred_username: Optional[str] = None # Shorthand name by which the End-User wishes to be referred to.
    profile: Optional[str] = None # URL of the End-User's profile page.
    picture: Optional[str] = None # URL of the End-User's profile picture.
    website: Optional[str] = None # URL of the End-User's Web page or blog.
    email: Optional[str] = None # End-User's preferred e-mail address.
    email_verified: Optional[bool] = None # True if the End-User's e-mail address has been verified.
    gender: Optional[str] = None # End-User's gender.
    birthdate: Optional[str] = None # End-User's birthday, YYYY-MM-DD format.
    zoneinfo: Optional[str] = None # String from zoneinfo time zone database.
    locale: Optional[str] = None # End-User's preferred locale.
    phone_number: Optional[str] = None # End-User's preferred telephone number.
    phone_number_verified: Optional[bool] = None # True if the End-User's phone number has been verified.
    address: Optional[Dict[str, Any]] = None # End-User's preferred postal address.
    updated_at: Optional[int] = None # Time the End-User's information was last updated, as a Unix timestamp.

    # Provider-specific fields can be added here if needed, or in a separate wrapper
    okta_profile_id: Optional[str] = None

    def to_dict(self) -> Dict[str, Any]:
        """Converts the dataclass instance to a dictionary, omitting None values."""
        return {k: v for k, v in self.__dict__.items() if v is not None}

@dataclass
class FederatedLoginEvent:
    """
    Represents an audit record for a federated login event.
    """
    event_id: str = field(default_factory=lambda: str(datetime.now().timestamp()))
    timestamp: datetime = field(default_factory=datetime.utcnow)
    provider: str # e.g., "Okta", "Google", "Auth0"
    user_id: str # The subject (sub) from the claims
    email: Optional[str] = None
    ip_address: Optional[str] = None
    user_agent: Optional[str] = None
    login_successful: bool = False
    claims: Optional[UserProfileClaims] = None
    # Additional context or metadata
    metadata: Dict[str, Any] = field(default_factory=dict)
    login_type: Optional[str] = None # e.g., "OAuth2", "PKCE", "SAML"

    def to_dict(self) -> Dict[str, Any]:
        data = {
            "event_id": self.event_id,
            "timestamp": self.timestamp.isoformat(),
            "provider": self.provider,
            "user_id": self.user_id,
            "email": self.email,
            "ip_address": self.ip_address,
            "user_agent": self.user_agent,
            "login_successful": self.login_successful,
            "login_type": self.login_type,
            "metadata": self.metadata
        }
        if self.claims:
            data["claims"] = self.claims.to_dict()
        return data

@dataclass
class AuditSummaryReport:
    """
    A summary report for login audit events.
    """
    report_id: str
    start_date: datetime
    end_date: datetime
    total_logins: int
    successful_logins: int
    failed_logins: int
    unique_users: int
    top_providers: List[Dict[str, Any]] # e.g., [{"provider": "Okta", "count": 100}]
    top_regions: List[Dict[str, Any]] # Based on IP geolocation if available
    summary_notes: Optional[str] = None

    def to_dict(self) -> Dict[str, Any]:
        return {
            "report_id": self.report_id,
            "start_date": self.start_date.isoformat(),
            "end_date": self.end_date.isoformat(),
            "total_logins": self.total_logins,
            "successful_logins": self.successful_logins,
            "failed_logins": self.failed_logins,
            "unique_users": self.unique_users,
            "top_providers": self.top_providers,
            "top_regions": self.top_regions,
            "summary_notes": self.summary_notes
        }
