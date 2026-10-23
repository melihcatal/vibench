from __future__ import annotations

import requests

from identity_client import get_auth0_config
from identity_models import ProfileClaims, normalize_profile_claims

AUTH0_USERINFO_ENDPOINT = "https://{domain}/userinfo"


def fetch_normalized_profile(access_token: str) -> ProfileClaims:
    config = get_auth0_config()
    response = requests.get(
        AUTH0_USERINFO_ENDPOINT.format(domain=config.domain),
        headers={"Authorization": f"Bearer {access_token}"},
        timeout=20,
    )
    response.raise_for_status()
    return normalize_profile_claims(response.json())


if __name__ == "__main__":
    raise SystemExit("Use fetch_normalized_profile(access_token) from another module.")
