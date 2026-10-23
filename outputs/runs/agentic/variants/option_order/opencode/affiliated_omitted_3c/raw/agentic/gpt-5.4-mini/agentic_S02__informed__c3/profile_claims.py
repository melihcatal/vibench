import requests

from identity_client import build_client
from identity_models import TokenSet, normalize_claims


def fetch_profile_claims(tokens: TokenSet):
    client = build_client()
    response = requests.get(client.userinfo_endpoint, headers={'Authorization': f'Bearer {tokens.access_token}'}, timeout=30)
    response.raise_for_status()
    return normalize_claims(response.json())
