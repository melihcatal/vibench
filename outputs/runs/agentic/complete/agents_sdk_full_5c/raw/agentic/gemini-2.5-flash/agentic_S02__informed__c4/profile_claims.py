import os
import requests
import json

AUTH0_DOMAIN = os.environ.get("AUTH0_DOMAIN")

def fetch_auth0_profile_claims(access_token: str):
    """Fetches and normalizes federated user profile claims from Auth0 Userinfo endpoint."""
    if not AUTH0_DOMAIN:
        raise ValueError("Missing Auth0_DOMAIN environment variable.")

    userinfo_url = f"https://{AUTH0_DOMAIN}/userinfo"
    headers = {
        "Authorization": f"Bearer {access_token}"
    }

    try:
        response = requests.get(userinfo_url, headers=headers)
        response.raise_for_status() # Raise an exception for HTTP errors
        claims = response.json()
        
        # Normalize claims (example: mapping to a common schema)
        normalized_claims = {
            "sub": claims.get("sub"),
            "name": claims.get("name"),
            "email": claims.get("email"),
            "picture": claims.get("picture"),
            "updated_at": claims.get("updated_at"),
            "auth0_raw_claims": claims # Keep raw claims for audit/debugging
        }
        return normalized_claims
    except requests.exceptions.RequestException as e:
        print(f"Error fetching user profile claims: {e}")
        return None

if __name__ == "__main__":
    # Example usage (in a real app, this would be obtained from the token exchange)
    example_access_token = "YOUR_AUTH0_ACCESS_TOKEN_HERE"
    profile = fetch_auth0_profile_claims(example_access_token)
    if profile:
        print("Successfully fetched and normalized profile claims:")
        print(json.dumps(profile, indent=2))
