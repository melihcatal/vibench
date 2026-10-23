import os
from typing import Dict, Any

# Provider: Google Identity Platform
GOOGLE_OAUTH2_ENDPOINT = "https://oauth2.googleapis.com/tokeninfo"
GOOGLE_USER_INFO_ENDPOINT = "https://openidconnect.googleapis.com/v1/userinfo"

ACCESS_TOKEN = os.getenv("GOOGLE_ACCESS_TOKEN")


def fetch_profile_claims(token: str) -> Dict[str, Any]:
    # Exchange token for federated profile (already done if token is valid)
    # Fetch normalized claims from Google user info endpoint
    resp = requests.get(GOOGLE_USER_INFO_ENDPOINT, params={"access_token": token})
    resp.raise_for_status()
    data = resp.json()
    # Normalize: ensure required keys exist
    normalized = {
        "sub": data.get("sub"),
        "email": data.get("email"),
        "name": data.get("name"),
        "profile_picture": data.get("picture"),
    }
    return normalized


if __name__ == "__main__":
    token = ACCESS_TOKEN
    if not token:
        raise ValueError("Google access token not set")
    claims = fetch_profile_claims(token)
    print("Federated claims:", claims)
