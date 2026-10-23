import requests
from identity_models import FederatedProfileResponse

# Use Google People API as the concrete provider for user profile claims
GOOGLE_PEOPLE_API = "https://people.googleapis.com/v1/people/me"
TOKEN_HEADER = "Authorization"
ACCESS_TOKEN_KEY = "access_token"


def fetch_federated_profile(access_token: str) -> FederatedProfileResponse:
    """
    Exchange an access_token for a normalized FederatedProfileResponse.
    """
    headers = {
        TOKEN_HEADER: f"Bearer {access_token}",
        "User-Agent": "FederatedLoginExample/1.0"
    }
    # The People API returns a JSON with a 'metadata' dict containing 'sources'.
    # We'll pull email, displayName and photoUrl and normalize them.
    resp = requests.get(GOOGLE_PEOPLE_API, headers=headers)
    resp.raise_for_status()
    data = resp.json()
    # Minimal extraction - adapt for other providers as needed
    sources = data.get("metadata", {}).get("sources", [])
    profile_sources = [source["type"] for source in sources]

    # Normalized claim set
    normalized = {
        "sub": data.get("resourceName", "unknown"),
        "email": data.get("emailAddresses", [{}])[0].get("value"),
        "name": data.get("names", [{}])[0].get("givenName")
        + " "
        + data.get("names", [{}])[0].get("familyName", ""),
        "picture": data.get("photos", [{}])[0].get("url"),
        "provider_sources": profile_sources,
    }
    return FederatedProfileResponse(**normalized)

# Example usage (not executed in library):
# profile = fetch_federated_profile(access_token)
# print(profile)
