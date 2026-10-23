from identity_client import get_json, load_config, userinfo_endpoint
from identity_models import normalize_profile_claims


def fetch_profile(access_token: str):
    config = load_config()
    claims = get_json(userinfo_endpoint(config), access_token)
    return normalize_profile_claims(claims)
