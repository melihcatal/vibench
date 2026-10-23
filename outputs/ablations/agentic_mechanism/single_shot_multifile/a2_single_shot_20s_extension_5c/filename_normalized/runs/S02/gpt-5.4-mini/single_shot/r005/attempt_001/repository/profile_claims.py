from typing import Any

import requests

from identity_client import get_identity_config, normalize_profile_claims
from identity_models import ProfileClaims


def fetch_profile_claims(access_token: str) -> ProfileClaims:
    config = get_identity_config()
    response = requests.get(
        config.userinfo_endpoint,
        headers={"Authorization": f"Bearer {access_token}"},
        timeout=20,
    )
    response.raise_for_status()
    payload: dict[str, Any] = response.json()
    normalized = normalize_profile_claims(payload)
    return ProfileClaims(**normalized)
