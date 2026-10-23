import requests

from identity_models import normalize_profile_claims


def profile_claims(payload, config=None):
    config = dict(config or {})
    response = requests.get("https://openidconnect.googleapis.com/v1/userinfo",
                            headers={"Authorization": f"Bearer {payload['access_token']}"}, timeout=30)
    response.raise_for_status()
    claims = response.json()
    return normalize_profile_claims(claims)
