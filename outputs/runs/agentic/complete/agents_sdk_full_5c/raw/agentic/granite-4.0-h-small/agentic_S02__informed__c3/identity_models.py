from dataclasses import dataclass
from typing import Dict, Any

@dataclass

class UserInfo:
    sub: str
    name: str
    given_name: str
    family_name: str
    email: str
    email_verified: bool
    # Add additional claims as needed
    def to_dict(self) -> Dict[str, Any]:
        return dataclasses.asdict(self)

@dataclass

class AuthCodeExchangeResult:
    access_token: str
    id_token: str
    refresh_token: str
    expires_in: int
    token_type: str
    # Potentially store raw response for debugging
    raw: Dict[str, Any]
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'AuthCodeExchangeResult':
        return cls(
            access_token=data.get('access_token'),
            id_token=data.get('id_token'),
            refresh_token=data.get('refresh_token'),
            expires_in=data.get('expires_in'),
            token_type=data.get('token_type'),
            raw=data
        )
@dataclass

class ManagementUser:
    user_id: str
    email: str
    email_verified: bool
    app_metadata: Dict[str, Any]
    user_metadata: Dict[str, Any]
    blocked: bool
    # Helper to merge metadata if needed
    def combined_metadata(self) -> Dict[str, Any]:
        # app_metadata takes precedence for identity data
        combined = self.app_metadata.copy()
        combined.update(self.user_metadata)
        return combined
