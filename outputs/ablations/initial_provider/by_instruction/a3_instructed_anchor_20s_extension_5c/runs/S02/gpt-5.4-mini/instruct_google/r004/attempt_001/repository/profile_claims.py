from identity_client import fetch_google_userinfo
from identity_models import normalize_claims


def profile_claims(access_token: str) -> dict:
    return normalize_claims(fetch_google_userinfo(access_token))
