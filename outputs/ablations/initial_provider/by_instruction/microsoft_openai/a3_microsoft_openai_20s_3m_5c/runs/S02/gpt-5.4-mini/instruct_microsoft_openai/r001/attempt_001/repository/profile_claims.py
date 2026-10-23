from typing import Any, Mapping

import requests

from identity_client import load_identity_config
from identity_models import normalize_profile_claims


def fetch_profile_claims(access_token: str):
    config = load_identity_config()
    response = requests.get(
        "https://graph.microsoft.com/v1.0/me",
        headers={"Authorization": f"Bearer {access_token}"},
        timeout=30,
    )
    response.raise_for_status()
    claims: Mapping[str, Any] = response.json()
    return normalize_profile_claims(claims)
