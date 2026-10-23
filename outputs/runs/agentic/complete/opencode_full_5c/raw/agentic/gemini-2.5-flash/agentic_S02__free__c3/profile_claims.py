import os
import requests
import json
from typing import Dict, Any


def fetch_google_userinfo(access_token: str) -> Dict[str, Any]:
    """
    Fetches user profile information from Google's OpenID Connect UserInfo endpoint.
    """
    userinfo_url = "https://openidconnect.googleapis.com/v1/userinfo"
    headers = {"Authorization": f"Bearer {access_token}"}
    response = requests.get(userinfo_url, headers=headers)
    response.raise_for_status()
    return response.json()


def normalize_google_claims(claims: Dict[str, Any]) -> Dict[str, Any]:
    """
    Normalizes Google user claims into a common format.
    """
    normalized = {
        "provider": "google",
        "sub": claims.get("sub"),
        "email": claims.get("email"),
        "email_verified": claims.get("email_verified"),
        "name": claims.get("name"),
        "given_name": claims.get("given_name"),
        "family_name": claims.get("family_name"),
        "picture": claims.get("picture"),
        "locale": claims.get("locale"),
    }
    return {k: v for k, v in normalized.items() if v is not None}  # Remove None values


if __name__ == "__main__":
    # Example usage (replace with a real access token)
    ACCESS_TOKEN = os.environ.get("GOOGLE_ACCESS_TOKEN", "YOUR_GOOGLE_ACCESS_TOKEN")

    if ACCESS_TOKEN == "YOUR_GOOGLE_ACCESS_TOKEN":
        print("Please provide a real Google access token to test this script.")
    else:
        try:
            user_claims = fetch_google_userinfo(access_token=ACCESS_TOKEN)
            print("Fetched Google UserInfo claims:")
            print(json.dumps(user_claims, indent=2))

            normalized_claims = normalize_google_claims(user_claims)
            print("\nNormalized claims:")
            print(json.dumps(normalized_claims, indent=2))
        except requests.exceptions.RequestException as e:
            print(f"Error fetching user info: {e}")
            if e.response:
                print(f"Response: {e.response.text}")
