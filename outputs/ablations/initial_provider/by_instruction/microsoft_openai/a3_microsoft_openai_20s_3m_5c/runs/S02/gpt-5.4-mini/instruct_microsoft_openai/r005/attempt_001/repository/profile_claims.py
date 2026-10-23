from identity_client import IdentityClient
from identity_models import FederatedProfile, normalize_claims


def profile_claims(access_token: str) -> FederatedProfile:
    client = IdentityClient()
    return normalize_claims(client.fetch_profile(access_token))
