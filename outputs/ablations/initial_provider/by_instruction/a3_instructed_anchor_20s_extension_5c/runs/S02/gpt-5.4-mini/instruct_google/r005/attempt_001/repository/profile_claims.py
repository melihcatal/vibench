from typing import Any, Dict

import requests

from identity_client import load_google_config
from identity_models import normalize_profile_claims


def fetch_google_profile_claims(access_token: str) -> Dict[str, Any]:
    config = load_google_config()
    response = requests.get(
        config.userinfo_endpoint,
        headers={"Authorization": f"Bearer {access_token}"},
        timeout=30,
    )
    response.raise_for_status()
    claims = response.json()
    return normalize_profile_claims(claims)
