import requests
from identity_models import normalize_claims


def profile_claims(payload, config=None):
    response = requests.get(
        "https://openidconnect.googleapis.com/v1/userinfo",
        headers={"Authorization": f"Bearer {payload['access_token']}"},
        timeout=30,
    )
    response.raise_for_status()
    return normalize_claims(response.json())
