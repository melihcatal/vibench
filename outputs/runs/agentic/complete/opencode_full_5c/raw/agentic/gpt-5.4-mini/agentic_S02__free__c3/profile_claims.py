from identity_client import fetch_userinfo
from identity_models import normalize_profile_claims


def get_profile_claims(access_token: str) -> dict:
    return normalize_profile_claims(fetch_userinfo(access_token))
