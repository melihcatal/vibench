import json
from identity_client import IdentityClient  # local helper

# IBM App ID Federation credentials (example environment variables)
CLIENT_ID = "IBM_APPID_CLIENT_ID"
CLIENT_SECRET = "IBM_APPID_CLIENT_SECRET"
AUTH_URL = "https://iam.test.cloud.ibm.com/identity/token"

app = IdentityClient(
    base_url=AUTH_URL, client_id=CLIENT_ID, client_secret=CLIENT_SECRET
)


def fetch_and_normalize_profile(access_token):
    """Fetch the user profile from IBM App ID and normalize to internal claims.

    Returns a dict with standard OIDC claim names.
    """
    profile_resp = app.get_userinfo(access_token=access_token)
    if not profile_resp.ok:
        raise RuntimeError(f"Failed to fetch userinfo: {profile_resp.text}")
    profile = profile_resp.json()
    # Normalize IBM App ID fields to OIDC standard claims
    normalized = {
        "sub": profile.get("sub"),
        "email": profile.get("email"),
        "email_verified": profile.get("email_verified"),
        "name": profile.get("name"),
        "given_name": profile.get("given_name"),
        "family_name": profile.get("family_name"),
        "picture": profile.get("picture"),
        # any additional fields can be added here
    }
    return normalized
