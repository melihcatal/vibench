from typing import Dict, Any, Optional

class OAuthCallbackRequest:
    def __init__(self, code: str, state: str, redirect_uri: str):
        self.code = code
        self.state = state
        self.redirect_uri = redirect_uri

class OAuthTokensResponse:
    def __init__(self, access_token: str, id_token: str, refresh_token: str, expires_in: int, token_type: str):
        self.access_token = access_token
        self.id_token = id_token
        self.refresh_token = refresh_token
        self.expires_in = expires_in
        self.token_type = token_type

class ProfileClaimsResponse:
    def __init__(self,
                 sub: str,
                 email: Optional[str] = None,
                 email_verified: Optional[bool] = None,
                 name: Optional[str] = None,
                 given_name: Optional[str] = None,
                 family_name: Optional[str] = None,
                 preferred_username: Optional[str] = None,
                 locale: Optional[str] = None,
                 picture: Optional[str] = None,
                 raw_claims: Optional[Dict[str, Any]] = None):
        self.sub = sub
        self.email = email
        self.email_verified = email_verified
        self.name = name
        self.given_name = given_name
        self.family_name = family_name
        self.preferred_username = preferred_username
        self.locale = locale
        self.picture = picture
        self.raw_claims = raw_claims

class PKCELoginRequest:
    def __init__(self, redirect_uri: str, identity_provider: Optional[str] = None):
        self.redirect_uri = redirect_uri
        self.identity_provider = identity_provider

class LoginAuditRecord:
    def __init__(self,
                 user_id: str,
                 timestamp: str,
                 event_type: str,
                 ip_address: str,
                 user_agent: str,
                 details: Optional[Dict[str, Any]] = None):
        self.user_id = user_id
        self.timestamp = timestamp
        self.event_type = event_type
        self.ip_address = ip_address
        self.user_agent = user_agent
        self.details = details
