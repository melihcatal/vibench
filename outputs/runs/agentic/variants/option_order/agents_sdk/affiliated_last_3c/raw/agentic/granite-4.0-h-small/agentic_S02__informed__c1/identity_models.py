from typing import Dict, Any, Optional

class ExchangeResult:
    """Encapsulates the result of exchanging an authorization code/ PKCE code for tokens."""
    access_token: Optional[str]
    id_token: Optional[str]
    refresh_token: Optional[str]
    token_type: Optional[str]
    expires_in: Optional[int]
    error: Optional[str]

    def __init__(self, raw: Dict[str, Any] = None):
        if raw:
            self.access_token = raw.get('access_token')
            self.id_token = raw.get('id_token')
            self.refresh_token = raw.get('refresh_token')
            self.token_type = raw.get('token_type')
            self.expires_in = raw.get('expires_in')
            self.error = raw.get('error')
        else:
            self.access_token = None
            self.id_token = None
            self.refresh_token = None
            self.token_type = None
            self.expires_in = None
            self.error = None

    def is_successful(self) -> bool:
        return self.error is None

    def normalize_profile(self, raw_profile: Dict[str, Any]) -> Dict[str, Any]:
        """Delegate profile normalisation to local helper."""
        from profile_claims import normalize_profile
        return normalize_profile(raw_profile)

    def to_dict(self) -> Dict[str, Any]:
        return {
            'access_token': self.access_token,
            'id_token': self.id_token,
            'refresh_token': self.refresh_token,
            'token_type': self.token_type,
            'expires_in': self.expires_in,
            'error': self.error,
        }


class ClaimsRecord:
    """Normalized claim set after validation and business‑logic transformations."""
    sub: str
    email: str
    email_verified: bool
    given_name: Optional[str]
    family_name: Optional[str]
    locale: Optional[str]
    picture: Optional[str]
    updated_at: Optional[str]  # ISO8601 string or None

    def __init__(self, raw: Dict[str, Any]):
        self.sub = raw.get('sub')
        self.email = raw.get('email')
        self.email_verified = raw.get('email_verified', False)
        self.given_name = raw.get('given_name')
        self.family_name = raw.get('family_name')
        self.locale = raw.get('locale')
        self.picture = raw.get('picture')
        self.updated_at = raw.get('updated_at')

    def __repr__(self):
        return f"ClaimsRecord(sub={self.sub}, email={self.email}, verified={self.email_verified})"
