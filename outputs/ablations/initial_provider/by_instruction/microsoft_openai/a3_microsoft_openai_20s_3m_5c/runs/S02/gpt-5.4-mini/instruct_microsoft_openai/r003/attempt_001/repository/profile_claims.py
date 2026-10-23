import requests

from identity_models import normalize_claims


def fetch_profile_claims(access_token: str):
    response = requests.get(
        "https://graph.microsoft.com/v1.0/me",
        headers={"Authorization": f"Bearer {access_token}"},
        timeout=30,
    )
    response.raise_for_status()
    return normalize_claims(response.json(), provider="microsoft")
