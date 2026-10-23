from __future__ import annotations
from dataclasses import dataclass, asdict
from typing import Any, Dict, Optional

@dataclass
class FederatedProfile:
    """Normalized representation of a federated identity profile."""
    sub: str  # unique identifier (often user_id or subject)
    email: Optional[str] = None
    email_verified: Optional[bool] = None
    name: Optional[str] = None
    given_name: Optional[str] = None
    family_name: Optional[str] = None
    nickname: Optional[str] = None
    picture: Optional[str] = None
    # Custom/optional claims are stored as a dict
    custom: Dict[str, Any] = dataclass(field_default=dict)

    @property
def dict(self) -> Dict[str, Any]:
        """Flatten the instance into a plain dict suitable for JSON serialization."""
        d = {
            'sub': self.sub,
            'email': self.email,
            'email_verified': self.email_verified,
            'name': self.name,
            'given_name': self.given_name,
            'family_name': self.family_name,
            'nickname': self.nickname,
            'picture': self.picture,
        }
        # Merge custom claims, preferring top‑level fields if duplicated
        d.update(self.custom)
        return d

    def __repr__(self) -> str:
        return f"FederatedProfile({asdict(self)})"

# ---------------------------------------------------------------------------
# Payload normalizers (simple examples)
# ---------------------------------------------------------------------------
def normalize_auth0_response(resp: Dict[str, Any]) -> FederatedProfile:
    """Convert raw Auth0 /userinfo response into FederatedProfile."""
    return FederatedProfile(
        sub=resp.get('sub'),
        email=resp.get('email'),
        email_verified=resp.get('email_verified'),
        name=resp.get('name'),
        given_name=resp.get('given_name'),
        family_name=resp.get('family_name'),
        nickname=resp.get('nickname'),
        picture=resp.get('picture'),
        custom={k: v for k, v in resp.items() if k not in {
            'sub', 'email', 'email_verified', 'name',
            'given_name', 'family_name', 'nickname', 'picture',
        }},
    )

# ---------------------------------------------------------------------------
# Example / sanity check
# ---------------------------------------------------------------------------
if __name__ == '__main__':
    demo_payload = {
        'sub': 'auth0|1234567890',
        'email': 'alice@example.com',
        'email_verified': True,
        'name': 'Alice Liddell',
        'given_name': 'Alice',
        'family_name': 'Liddell',
        'nickname': 'al84',
        'picture': 'https://example.com/avatar.jpg',
        'role': 'admin',  # custom claim example
    }
    profile = normalize_auth0_response(demo_payload)
    print('Normalized profile:', profile)
