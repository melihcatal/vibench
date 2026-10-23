import json
import urllib.request

from identity_client import load_identity_config
from identity_models import normalize_profile_claims


def fetch_and_normalize_profile_claims(access_token: str):
    cfg = load_identity_config()
    req = urllib.request.Request(
        cfg.userinfo_url,
        headers={"Authorization": f"Bearer {access_token}"},
        method="GET",
    )
    with urllib.request.urlopen(req, timeout=30) as resp:
        raw = json.loads(resp.read().decode())
    return normalize_profile_claims(raw)
