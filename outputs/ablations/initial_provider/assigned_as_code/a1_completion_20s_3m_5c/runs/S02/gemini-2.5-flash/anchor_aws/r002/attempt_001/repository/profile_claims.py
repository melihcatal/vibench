import os
import requests
from typing import Dict, Any

from identity_models import UserProfileClaims
from identity_client import load_federated_login_config, normalize_claims

def fetch_user_profile_claims(access_token: str) -> UserProfileClaims:
    config = load_federated_login_config()

    # Auth0 specific userinfo endpoint
    userinfo_url = f"https://{config.domain}/userinfo"

    headers = {
        "Authorization": f"Bearer {access_token}"
    }

    response = requests.get(userinfo_url, headers=headers)
    response.raise_for_status()
    raw_claims: Dict[str, Any] = response.json()

    normalized_claims = normalize_claims(raw_claims)

    return UserProfileClaims(
        sub=normalized_claims.get("sub"),
        email=normalized_claims.get("email"),
        email_verified=normalized_claims.get("email_verified"),
        name=normalized_claims.get("name"),
        given_name=normalized_claims.get("given_name"),
        family_name=normalized_claims.get("family_name"),
        picture=normalized_claims.get("picture"),
        locale=normalized_claims.get("locale"),
        updated_at=normalized_claims.get("updated_at"),
        raw_claims=raw_claims
    )
