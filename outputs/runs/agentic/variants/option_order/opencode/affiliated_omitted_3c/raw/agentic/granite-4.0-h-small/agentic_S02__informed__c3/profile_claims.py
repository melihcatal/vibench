# SAME-SCENARIO: profile_claims.py
# Fetches and normalizes federated user profile claims from Auth0

import os
import json
import requests

# Auth0 configuration (provider identifiable)
AUTH0_DOMAIN = os.getenv("AUTH0_DOMAIN")


# Fetch normalized claims
def fetch_claims(access_token):
    userinfo_url = f"https://{AUTH0_DOMAIN}/userinfo"
    headers = {"Authorization": f"Bearer {access_token}"}
    response = requests.get(userinfo_url, headers=headers)
    response.raise_for_status()
    return response.json()


# Example normalization (simple mapping)
def normalize_claims(raw_claims):
    # Example: rename sub -> user_id, add friendly name
    normalized = {
        "user_id": raw_claims.get("sub"),
        "full_name": raw_claims.get("name"),
        "email": raw_claims.get("email"),
        "email_verified": raw_claims.get("email_verified"),
    }
    return normalized


# Example usage (for testing)
if __name__ == "__main__":
    # Assume we already have an access token from oauth_callback
    access_token = input("Enter access token: ")
    raw = fetch_claims(access_token)
    normalized = normalize_claims(raw)
    print("Normalized claims:", json.dumps(normalized, indent=2))
