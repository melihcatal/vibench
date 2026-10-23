from dataclasses import dataclass
from typing import Dict, Any

@dataclass
class UserTokens:
    access_token: str
    id_token: str
    refresh_token: str
    expires_in: int

def parse_auth_result(auth_result: Dict[str, Any]) -> UserTokens:
    return UserTokens(
        access_token=auth_result['AccessToken'],
        id_token=auth_result['IdToken'],
        refresh_token=auth_result['RefreshToken'],
        expires_in=auth_result['ExpiresIn']
    )