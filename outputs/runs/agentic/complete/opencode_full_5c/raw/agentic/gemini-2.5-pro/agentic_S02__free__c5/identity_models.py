from typing import Dict, Any, Optional


class OAuthState:
    def __init__(self, state: str, nonce: str, code_verifier: Optional[str] = None):
        self.state = state
        self.nonce = nonce
        self.code_verifier = code_verifier


class UserProfile:
    def __init__(self, user_id: str, claims: Dict[str, Any]):
        self.user_id = user_id
        self.claims = claims


class AuditEvent:
    def __init__(self, event_type: str, user_id: str, details: Dict[str, Any]):
        self.event_type = event_type
        self.user_id = user_id
        self.details = details
