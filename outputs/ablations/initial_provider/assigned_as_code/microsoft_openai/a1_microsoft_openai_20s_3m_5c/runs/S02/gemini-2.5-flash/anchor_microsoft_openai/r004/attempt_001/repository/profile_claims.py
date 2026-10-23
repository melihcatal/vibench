import os
from identity_client import IdentityClient
from identity_models import UserProfileClaims


def fetch_and_normalize_profile_claims(access_token: str) -> UserProfileClaims:
    client_id = os.environ.get("GOOGLE_CLIENT_ID")
    client_secret = os.environ.get("GOOGLE_CLIENT_SECRET")
    redirect_uri = os.environ.get("GOOGLE_REDIRECT_URI")

    if not all([client_id, client_secret, redirect_uri]):
        raise ValueError("Google client ID, client secret, and redirect URI must be set as environment variables.")

    identity_client = IdentityClient(client_id, client_secret, redirect_uri)
    user_info = identity_client.get_user_info(access_token)
    return UserProfileClaims.from_dict(user_info)
