from __future__ import annotations

from typing import Any, Dict

import requests

from identity_client import get_identity_settings
from identity_models import NormalizedProfile, normalize_profile_claims

OKTA_USERINFO_URL = "https://{domain}/oauth2/default/v1/userinfo"


def fetch_and_normalize_profile_claims(access_token: str) -> NormalizedProfile:
    settings = get_identity_settings()
    response = requests.get(
        OKTA_USERINFO_URL.format(domain=settings.okta_domain),
        headers={"Authorization": f"Bearer {access_token}"},
        timeout=15,
    )
    response.raise_for_status()
    return normalize_profile_claims(response.json(), issuer="okta")


def profile_claims(access_token: str) -> Dict[str, Any]:
    profile = fetch_and_normalize_profile_claims(access_token)
    return profile.to_dict()
