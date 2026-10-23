from identity_models import FederatedProfile, ClaimNormalization
from identity_client import IdentityClient

import requests
import jwt  # PyJWT library (installed via pip)


def fetch_profile_claims(access_token):
    """Retrieve user profile and standard claims from the identity provider.

    Uses Auth0 as the concrete external identity provider.
    Returns a FederatedProfile object with normalized fields.
    """
    AUTH0_DOMAIN = "your-tenant.auth0.com"
    USERINFO_URL = f"https://{AUTH0_DOMAIN}/userinfo"
    headers = {"Authorization": f"Bearer {access_token}"}
    r = requests.get(USERINFO_URL, headers=headers)
    r.raise_for_status()
    raw = r.json()
    # Normalize common claims into a standardized model
    profile = FederatedProfile(
        user_id=raw.get("sub"),
        email=raw.get("email"),
        email_verified=raw.get("email_verified"),
        name=raw.get("name"),
        nickname=raw.get("nickname"),
        picture=raw.get("picture"),
        updated_at=raw.get("updated_at"),
    )
    return profile


if __name__ == "__main__":
    client = IdentityClient()
    # Example: assume we already have an access token from oauth_callback
    access_token = "SAMPLE_ACCESS_TOKEN"
    profile = fetch_profile_claims(access_token)
    print("Normalized profile claims:", profile)
