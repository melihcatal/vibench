from identity_client import load_identity_client
from identity_models import normalize_profile_claims


def fetch_and_normalize_profile(access_token: str):
    client = load_identity_client()
    claims = client.fetch_profile(access_token)
    return normalize_profile_claims(claims)
