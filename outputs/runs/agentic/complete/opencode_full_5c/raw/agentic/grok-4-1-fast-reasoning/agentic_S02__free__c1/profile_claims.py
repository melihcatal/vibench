import requests
from identity_models import UserClaims, normalize_claims


def fetch_profile_claims(access_token: str) -> UserClaims:
    headers = {
        "Authorization": f"Bearer {access_token}",
    }
    response = requests.get(
        "https://openidconnect.googleapis.com/v1/userinfo",
        headers=headers,
    )
    response.raise_for_status()
    raw_claims = response.json()
    return normalize_claims(raw_claims)
