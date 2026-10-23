from identity_client import fetch_google_userinfo
from identity_models import normalize_profile


def profile_claims(access_token: str) -> dict[str, object]:
    claims = fetch_google_userinfo(access_token)
    return normalize_profile(claims)
