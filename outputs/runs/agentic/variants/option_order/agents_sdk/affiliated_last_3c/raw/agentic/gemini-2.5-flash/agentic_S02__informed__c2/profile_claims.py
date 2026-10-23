import os
import requests
from typing import Dict, Any

def fetch_and_normalize_profile_claims(access_token: str) -> Dict[str, Any]:
    """
    Fetches user profile claims from Auth0's /userinfo endpoint
    and normalizes them into a consistent dictionary format.
    """
    AUTH0_DOMAIN = os.environ.get("AUTH0_DOMAIN")
    if not AUTH0_DOMAIN:
        raise ValueError("Missing Auth0_DOMAIN environment variable.")

    userinfo_url = f"https://{AUTH0_DOMAIN}/userinfo"
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }

    try:
        response = requests.get(userinfo_url, headers=headers)
        response.raise_for_status()
        claims = response.json()
        
        # Normalize claims
        normalized_claims = {
            "sub": claims.get("sub"),
            "name": claims.get("name"),
            "given_name": claims.get("given_name"),
            "family_name": claims.get("family_name"),
            "email": claims.get("email"),
            "email_verified": claims.get("email_verified"),
            "picture": claims.get("picture"),
            "locale": claims.get("locale"),
            # Add any other claims you want to normalize
            "raw_claims": claims # Keep raw claims for completeness
        }
        return normalized_claims
    except requests.exceptions.RequestException as e:
        print(f"Error fetching userinfo: {e}")
        if response is not None:
            print(f"Response content: {response.text}")
        raise

if __name__ == "__main__":
    # Example usage
    os.environ["AUTH0_DOMAIN"] = "YOUR_AUTH0_DOMAIN.us.auth0.com"
    
    # In a real scenario, this access_token would come from the oauth_callback.py step
    mock_access_token = "eyJhbGciOiJSUzI1NiIsImtpZCI6IkF...YOUR_MOCK_ACCESS_TOKEN" 
    
    try:
        profile = fetch_and_normalize_profile_claims(mock_access_token)
        import json
        print("Normalized User Profile Claims:")
        print(json.dumps(profile, indent=2))
    except ValueError as e:
        print(f"Configuration Error: {e}")
    except Exception as e:
        print(f"Runtime Error: {e}")
