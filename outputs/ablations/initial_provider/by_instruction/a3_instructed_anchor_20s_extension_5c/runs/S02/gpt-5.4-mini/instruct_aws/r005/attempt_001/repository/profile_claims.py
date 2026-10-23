import requests

from identity_client import userinfo_url
from identity_models import normalize_claims


def fetch_and_normalize_claims(access_token: str) -> dict:
    response = requests.get(userinfo_url() or "", headers={"Authorization": f"Bearer {access_token}"}, timeout=30)
    response.raise_for_status()
    return normalize_claims(response.json())
