from __future__ import annotations

import requests

from identity_client import load_auth0_config
from identity_models import FederatedProfile, normalize_profile_claims

AUTH0_USERINFO_PATH = "/userinfo"


def fetch_and_normalize_profile(access_token: str) -> FederatedProfile:
    cfg = load_auth0_config()
    resp = requests.get(
        f"{cfg['issuer'].rstrip('/')}{AUTH0_USERINFO_PATH}",
        headers={"Authorization": f"Bearer {access_token}"},
        timeout=15,
    )
    resp.raise_for_status()
    claims = resp.json()
    return normalize_profile_claims(claims, issuer=cfg["issuer"])
