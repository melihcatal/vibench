from typing import Dict, Any, Optional
from dataclasses import dataclass

@dataclass
class AuthTokens:
    access_token: str
    id_token: Optional[str] = None
    refresh_token: Optional[str] = None
    token_type: Optional[str] = None
    expires_in: Optional[int] = None

@dataclass
class UserProfileClaims:
    user_id: str
    email: Optional[str] = None
    name: Optional[str] = None
    picture: Optional[str] = None
    raw_claims: Dict[str, Any] = None

    @staticmethod
    def from_auth0_claims(claims: Dict[str, Any]) -> 'UserProfileClaims':
        return UserProfileClaims(
            user_id=claims.get("sub"),
            email=claims.get("email"),
            name=claims.get("name"),
            picture=claims.get("picture"),
            raw_claims=claims
        )


if __name__ == '__main__':
    # Example usage:
    # tokens = AuthTokens(
    #     access_token="a.b.c",
    #     id_token="d.e.f",
    #     expires_in=3600
    # )
    # print(tokens)
    #
    # auth0_sample_claims = {
    #     "sub": "auth0|12345",
    #     "name": "Test User",
    #     "email": "test@example.com",
    #     "picture": "http://example.com/pic.jpg",
    #     "updated_at": "2023-01-01T12:00:00.000Z"
    # }
    # profile = UserProfileClaims.from_auth0_claims(auth0_sample_claims)
    # print(profile)
    pass
