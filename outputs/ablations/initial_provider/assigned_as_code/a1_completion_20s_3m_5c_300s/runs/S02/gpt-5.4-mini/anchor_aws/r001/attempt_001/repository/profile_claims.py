import requests

from identity_models import normalize_identity_profile


def profile_claims(payload, config=None):
    config = config or {}
    userinfo_url = f"https://{config['domain_prefix']}.auth.{config['region']}.amazoncognito.com/oauth2/userInfo"
    headers = {"Authorization": f"Bearer {payload['access_token']}"}
    response = requests.get(userinfo_url, headers=headers, timeout=15)
    response.raise_for_status()
    return normalize_identity_profile(response.json())
