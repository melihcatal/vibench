from __future__ import annotations

from typing import Dict, Optional

from identity_client import Auth0OIDCClient
from identity_models import NormalizedProfile, normalize_boolean


class FederatedProfileClaims:
    def __init__(self, client: Optional[Auth0OIDCClient] = None):
        self.client = client or Auth0OIDCClient()

    def fetch_and_normalize(self, access_token: str) -> Dict[str, object]:
        claims = self.client.fetch_userinfo(access_token)
        profile = NormalizedProfile(
            subject=claims["sub"],
            email=claims.get("email"),
            email_verified=normalize_boolean(claims.get("email_verified")),
            name=claims.get("name"),
            given_name=claims.get("given_name"),
            family_name=claims.get("family_name"),
            picture=claims.get("picture"),
            locale=claims.get("locale"),
            provider="Auth0 Authentication API",
            raw_claims=claims,
        )
        return {
            "subject": profile.subject,
            "email": profile.email,
            "email_verified": profile.email_verified,
            "name": profile.name,
            "given_name": profile.given_name,
            "family_name": profile.family_name,
            "picture": profile.picture,
            "locale": profile.locale,
            "provider": profile.provider,
            "raw_claims": profile.raw_claims,
        }
