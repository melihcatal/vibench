import json
from typing import TypedDict

# Simple request/response data models used throughout the flow

class LoginRequest(TypedDict):
    username: str
    password: str

class TokenResponse(TypedDict):
    access_token: str
    token_type: str
    expires_in: int
    refresh_token: str

class ProfileResponse(TypedDict):
    sub: str
    name: str
    email: str
    picture: str
    locale: str

class AuditEvent(TypedDict):
    event_id: str
    event_type: str
    timestamp: str
    details: Dict[str, Any]

# Example functions for normalization may reference these models
if __name__ == '__main__':
    sample_event = {
        'event_id': 'evt_001',
        'event_type': 'login',
        'timestamp': '2025-01-01T12:34:56Z',
        'details': {'user_id': '123', 'method': 'password'}
    }
    print(json.dumps(sample_event, indent=2))