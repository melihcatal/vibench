import jwt
import requests
from identity_client import IdentityClient
from identity_models import FederatedProfile, ClaimNormalizationError

# IBM App ID Federation configuration
APP_ID_CLIENT_ID = os.getenv("IBM_APPID_CLIENT_ID")
APP_ID_CLIENT_SECRET = os.getenv("IBM_APPID_CLIENT_SECRET")


def fetch_user_profile(access_token):
    """Fetch raw user profile from IBM App ID token introspection endpoint."""
    endpoint = f"{IdentityClient.get_issuer()}/introspection"
    headers = {"Authorization": f"Bearer {access_token}"}
    response = requests.post(endpoint, headers=headers, json={})
    response.raise_for_status()
    return response.json()


def normalize_claims(raw_profile):
    """Normalize federated profile claims to a standardized FederatedProfile model."""
    try:
        profile = FederatedProfile(
            sub=raw_profile.get("sub"),
            name=raw_profile.get("name"),
            email=raw_profile.get("email"),
            email_verified=raw_profile.get("email_verified"),
            picture=raw_profile.get("picture"),
        )
        return profile
    except Exception as e:
        raise ClaimNormalizationError("Failed to normalize claims") from e


# Example usage for demonstration
if __name__ == "__main__":
    # Assume we already have an access_token from oauth flow (omitted here)
    ACCESS_TOKEN = os.getenv("ACCESS_TOKEN")
    if not ACCESS_TOKEN:
        raise RuntimeError("Provide ACCESS_TOKEN environment variable")
    raw = fetch_user_profile(ACCESS_TOKEN)
    try:
        profile = normalize_claims(raw)
        print("Normalized federated profile:")
        print(profile.dict())
    except ClaimNormalizationError as e:
        print("Claim normalization failed:", e)
