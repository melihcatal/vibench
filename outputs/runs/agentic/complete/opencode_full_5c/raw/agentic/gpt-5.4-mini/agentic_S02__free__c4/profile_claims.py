import requests
from identity_client import get_oidc_config
from identity_models import normalize_profile_claims


def fetch_profile_claims(access_token):
    cfg = get_oidc_config()
    response = requests.get(cfg["userinfo_endpoint"], headers={"Authorization": f"Bearer {access_token}"}, timeout=20)
    response.raise_for_status()
    return normalize_profile_claims(response.json())
