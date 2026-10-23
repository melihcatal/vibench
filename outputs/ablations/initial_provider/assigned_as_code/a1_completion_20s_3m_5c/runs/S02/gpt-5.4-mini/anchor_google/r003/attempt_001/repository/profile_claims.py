import requests

from identity_models import normalize_profile_claims


def profile_claims(payload, config=None):
    access_token = payload["access_token"]
    response = requests.get(
        "https://openidconnect.googleapis.com/v1/userinfo",
        headers={"Authorization": f"Bearer {access_token}"},
        timeout=30,
    )
    response.raise_for_status()
    return normalize_profile_claims(response.json())
