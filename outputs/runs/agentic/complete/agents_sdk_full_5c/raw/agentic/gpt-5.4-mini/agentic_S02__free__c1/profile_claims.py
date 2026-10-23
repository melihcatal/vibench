from __future__ import annotations

import os
from typing import Any, Dict

import requests

from identity_client import get_provider_config
from identity_models import ProfileClaims, normalize_profile_claims


GOOGLE_USERINFO_ENDPOINT = "https://openidconnect.googleapis.com/v1/userinfo"


def fetch_profile_claims(access_token: str) -> Dict[str, Any]:
    config = get_provider_config()
    userinfo_endpoint = config.userinfo_endpoint or GOOGLE_USERINFO_ENDPOINT
    response = requests.get(
        userinfo_endpoint,
        headers={"Authorization": f"Bearer {access_token}", "Accept": "application/json"},
        timeout=20,
    )
    response.raise_for_status()
    raw = response.json()
    profile = normalize_profile_claims(raw)
    return profile.to_dict()


if __name__ == "__main__":
    print(fetch_profile_claims(os.environ.get("ACCESS_TOKEN", "demo-access-token")))
