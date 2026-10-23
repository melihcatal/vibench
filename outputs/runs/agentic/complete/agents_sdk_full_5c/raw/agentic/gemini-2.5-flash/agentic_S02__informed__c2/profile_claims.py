import os
import requests
from typing import Dict, Any
from identity_client import AUTH0_DOMAIN
from identity_models import UserProfileClaims

def fetch_user_profile_claims(access_token: str) -> UserProfileClaims:
    """Fetches user profile claims from Auth0's /userinfo endpoint."""
    userinfo_url = f"https://{AUTH0_DOMAIN}/userinfo"
    headers = {"Authorization": f"Bearer {access_token}"}
    
    response = requests.get(userinfo_url, headers=headers)
    response.raise_for_status()
    
    claims_data = response.json()
    return UserProfileClaims(
        sub=claims_data.get("sub"),
        name=claims_data.get("name"),
        given_name=claims_data.get("given_name"),
        family_name=claims_data.get("family_name"),
        nickname=claims_data.get("nickname"),
        picture=claims_data.get("picture"),
        email=claims_data.get("email"),
        email_verified=claims_data.get("email_verified")
    )

def normalize_claims(claims: UserProfileClaims) -> Dict[str, Any]:
    """Normalizes the federated user profile claims into a simpler dictionary."""
    normalized = {
        "user_id": claims.sub,
        "display_name": claims.name,
        "first_name": claims.given_name,
        "last_name": claims.family_name,
        "email_address": claims.email,
        "email_verified": claims.email_verified,
        "profile_picture": claims.picture,
    }
    # Remove None values
    return {k: v for k, v in normalized.items() if v is not None}

if __name__ == "__main__":
    # This is a placeholder for demonstration. In a real app, 'access_token' would come from oauth_callback.
    print("Simulating fetching user claims. Please provide an access token.")
    # example_access_token = "YOUR_ACCESS_TOKEN_HERE"
    # try:
    #     claims = fetch_user_profile_claims(example_access_token)
    #     print("Raw claims:", claims)
    #     normalized_claims = normalize_claims(claims)
    #     print("Normalized claims:", normalized_claims)
    # except requests.exceptions.HTTPError as e:
    #     print(f"Error fetching claims: {e}")
    #     print(f"Response: {e.response.text}")
