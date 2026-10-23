from dataclasses import dataclass, field
from typing import Optional, Dict, Any

@dataclass
class UserProfile:
    provider: str
    sub: str
    email: Optional[str] = None
    email_verified: Optional[bool] = False
    name: Optional[str] = None
    given_name: Optional[str] = None
    family_name: Optional[str] = None
    picture: Optional[str] = None
    locale: Optional[str] = None
    raw_claims: Dict[str, Any] = field(default_factory=dict)

    @staticmethod
    def from_google_claims(claims: Dict[str, Any]) -> "UserProfile":
        return UserProfile(
            provider="google",
            sub=claims.get("sub", ""),
            email=claims.get("email"),
            email_verified=claims.get("email_verified"),
            name=claims.get("name"),
            given_name=claims.get("given_name"),
            family_name=claims.get("family_name"),
            picture=claims.get("picture"),
            locale=claims.get("locale"),
            raw_claims=claims
        )

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

if __name__ == "__main__":
    # Example Google claims
    google_claims_example = {
        "sub": "1234567890",
        "name": "John Doe",
        "given_name": "John",
        "family_name": "Doe",
        "picture": "https://example.com/john.jpg",
        "email": "john.doe@example.com",
        "email_verified": True,
        "locale": "en",
        "aud": "your_client_id",
        "iss": "https://accounts.google.com",
        "exp": 1678886400,
        "iat": 1678882800,
    }

    user_profile = UserProfile.from_google_claims(google_claims_example)
    print("Normalized User Profile:")
    print(user_profile.to_dict())
