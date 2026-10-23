import os
from typing import Any

import requests

from identity_client import build_oidc_config, normalize_claims_payload
from identity_models import FederatedProfile

USERINFO_ENDPOINT_OVERRIDE = os.environ.get("IDP_USERINFO_ENDPOINT", "")


def fetch_profile_claims(access_token: str) -> FederatedProfile:
    cfg = build_oidc_config()
    userinfo_endpoint = USERINFO_ENDPOINT_OVERRIDE or cfg.userinfo_endpoint()
    response = requests.get(userinfo_endpoint, headers={"Authorization": f"Bearer {access_token}"}, timeout=15)
    response.raise_for_status()
    payload: dict[str, Any] = response.json()
    normalized = normalize_claims_payload(payload)
    return FederatedProfile.from_claims(normalized)


def profile_as_dict(access_token: str) -> dict:
    return fetch_profile_claims(access_token).to_dict()
