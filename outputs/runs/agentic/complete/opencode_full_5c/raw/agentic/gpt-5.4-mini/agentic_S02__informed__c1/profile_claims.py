from typing import Any, Dict

import requests

from identity_client import load_config, userinfo_endpoint
from identity_models import normalize_profile_claims


def profile_claims(access_token: str) -> Dict[str, Any]:
    config = load_config()
    response = requests.get(
        userinfo_endpoint(config),
        headers={"Authorization": f"Bearer {access_token}"},
        timeout=30,
    )
    response.raise_for_status()
    return normalize_profile_claims(response.json())
