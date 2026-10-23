from __future__ import annotations

import requests

from identity_client import load_identity_config
from identity_models import NormalizedProfile, normalize_claims


def fetch_profile(access_token: str) -> NormalizedProfile:
    cfg = load_identity_config()
    userinfo_url = f"https://{cfg['issuer']}/userinfo" if not cfg["issuer"].startswith("https://") else f"{cfg['issuer']}/userinfo"
    resp = requests.get(userinfo_url, headers={"Authorization": f"Bearer {access_token}"}, timeout=20)
    resp.raise_for_status()
    return normalize_claims("auth0", resp.json())
