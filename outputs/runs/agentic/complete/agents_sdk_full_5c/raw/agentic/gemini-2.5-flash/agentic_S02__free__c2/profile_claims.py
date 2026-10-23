import os
import requests
import json

# Google Identity Platform UserInfo endpoint
GOOGLE_USERINFO_URL = "https://www.googleapis.com/oauth2/v3/userinfo"

def fetch_google_user_profile(access_token: str) -> dict:
    headers = {
        "Authorization": f"Bearer {access_token}"
    }
    try:
        response = requests.get(GOOGLE_USERINFO_URL, headers=headers)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error fetching Google user profile: {e}")
        return {"error": str(e)}

def normalize_profile_claims(raw_profile: dict) -> dict:
    """Normalizes Google user profile claims to a common format."""
    normalized_claims = {
        "provider": "google",
        "sub": raw_profile.get("sub"),
        "email": raw_profile.get("email"),
        "email_verified": raw_profile.get("email_verified", False),
        "name": raw_profile.get("name"),
        "given_name": raw_profile.get("given_name"),
        "family_name": raw_profile.get("family_name"),
        "picture": raw_profile.get("picture"),
        "locale": raw_profile.get("locale"),
    }
    return normalized_claims

if __name__ == "__main__":
    # Example usage (replace with actual access token)
    example_access_token = "ya29.a0AWY7Ckr..."
    print(f"Fetching user profile with example access token...")
    raw_profile = fetch_google_user_profile(example_access_token)
    print(f"Raw profile:\n{json.dumps(raw_profile, indent=2)}")
    
    if raw_profile and not raw_profile.get("error"):
        normalized_profile = normalize_profile_claims(raw_profile)
        print(f"\nNormalized profile:\n{json.dumps(normalized_profile, indent=2)}")
