import requests

from identity_client import GOOGLE_USERINFO_ENDPOINT
from identity_models import normalize_google_profile


def profile_claims(access_token: str):
    response = requests.get(
        GOOGLE_USERINFO_ENDPOINT,
        headers={"Authorization": f"Bearer {access_token}"},
        timeout=20,
    )
    response.raise_for_status()
    return normalize_google_profile(response.json())
