from __future__ import annotations

from typing import Dict

import requests

from identity_client import load_login_config
from identity_models import FederatedUserProfile, normalize_profile_claims

AUTH0_PROVIDER = "Auth0 Authentication API"


def fetch_and_normalize_profile(access_token: str) -> FederatedUserProfile:
    config = load_login_config()
    userinfo_url = f"{config.issuer.rstrip('/')}/userinfo"
    response = requests.get(userinfo_url, headers={"Authorization": f"Bearer {access_token}"}, timeout=10)
    response.raise_for_status()
    claims: Dict[str, object] = response.json()
    return normalize_profile_claims(claims)
