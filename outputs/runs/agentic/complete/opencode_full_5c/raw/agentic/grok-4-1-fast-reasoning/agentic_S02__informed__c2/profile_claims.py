import requests
from identity_client import USERINFO_ENDPOINT
from identity_models import UserProfile


def fetch_profile_claims(access_token: str) -> UserProfile:
    headers = {"Authorization": f"Bearer {access_token}"}
    response = requests.get(USERINFO_ENDPOINT, headers=headers)
    response.raise_for_status()
    claims = response.json()
    return UserProfile.from_claims(claims)
