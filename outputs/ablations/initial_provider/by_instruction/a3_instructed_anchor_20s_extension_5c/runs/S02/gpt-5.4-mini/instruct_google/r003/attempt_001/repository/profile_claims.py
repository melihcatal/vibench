from identity_client import fetch_userinfo, load_google_config
from identity_models import normalize_profile_claims


def profile_claims(access_token: str):
    config = load_google_config()
    claims = fetch_userinfo(config, access_token)
    return normalize_profile_claims(claims, issuer=config.issuer)
