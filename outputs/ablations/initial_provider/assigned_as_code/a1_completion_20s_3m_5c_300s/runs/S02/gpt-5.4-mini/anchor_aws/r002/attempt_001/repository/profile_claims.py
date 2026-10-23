import json
import urllib.request

from identity_client import load_identity_config
from identity_models import normalize_profile_claims


def profile_claims(payload, config=None):
    cfg = load_identity_config(config)
    request = urllib.request.Request(
        (cfg.issuer_url or "https://cognito-idp.amazonaws.com") + "/oauth2/userInfo",
        headers={"Authorization": f"Bearer {payload['access_token']}"},
    )
    with urllib.request.urlopen(request) as resp:
        claims = json.loads(resp.read().decode())
    return normalize_profile_claims(claims)
