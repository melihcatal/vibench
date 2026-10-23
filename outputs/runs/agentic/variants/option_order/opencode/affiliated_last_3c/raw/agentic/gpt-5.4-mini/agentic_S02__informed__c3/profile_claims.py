from identity_client import fetch_json, load_identity_config
from identity_models import normalize_profile_claims


def fetch_and_normalize_profile(access_token: str):
    config = load_identity_config()
    claims = fetch_json(config["userinfo_endpoint"], access_token)
    return normalize_profile_claims(claims)
