from identity_client import Auth0IdentityClient
from identity_models import normalize_claims


def fetch_normalized_claims(access_token: str):
    client = Auth0IdentityClient()
    claims = client.fetch_profile(access_token)
    return normalize_claims(claims)
