from identity_client import fetch_userinfo
from identity_models import normalize_claims


def fetch_profile_claims(access_token: str):
    payload = fetch_userinfo(access_token)
    return normalize_claims(payload, issuer="https://example.auth0.com/")
