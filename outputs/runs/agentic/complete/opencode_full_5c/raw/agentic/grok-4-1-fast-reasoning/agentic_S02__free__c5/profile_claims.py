import requests
from identity_models import UserProfile, parse_userinfo_response

GOOGLE_USERINFO_URL = "https://openidconnect.googleapis.com/v1/userinfo"


def fetch_and_normalize_profile_claims(access_token: str) -> UserProfile:
    headers = {"Authorization": f"Bearer {access_token}"}
    resp = requests.get(GOOGLE_USERINFO_URL, headers=headers)
    resp.raise_for_status()
    claims = resp.json()
    return parse_userinfo_response(claims)
