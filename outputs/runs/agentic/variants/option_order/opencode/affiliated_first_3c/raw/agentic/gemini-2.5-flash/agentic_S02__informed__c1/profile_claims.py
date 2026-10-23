import os
import requests

AUTH0_DOMAIN = os.environ.get("AUTH0_DOMAIN")


def fetch_user_profile_claims(access_token):
    if not AUTH0_DOMAIN:
        raise ValueError("Missing Auth0_DOMAIN environment variable.")

    userinfo_url = f"https://{AUTH0_DOMAIN}/userinfo"
    headers = {"Authorization": f"Bearer {access_token}"}

    try:
        response = requests.get(userinfo_url, headers=headers)
        response.raise_for_status()  # Raise HTTPError for bad responses (4xx or 5xx)
        claims = response.json()
        return normalize_claims(claims)
    except requests.exceptions.RequestException as e:
        print(f"Error fetching user info: {e}")
        return None


def normalize_claims(claims):
    # Basic normalization for Auth0 claims to a generic structure
    normalized = {
        "sub": claims.get("sub"),
        "name": claims.get("name"),
        "email": claims.get("email"),
        "email_verified": claims.get("email_verified"),
        "picture": claims.get("picture"),
        "given_name": claims.get("given_name"),
        "family_name": claims.get("family_name"),
        "locale": claims.get("locale"),
    }
    return {k: v for k, v in normalized.items() if v is not None}


if __name__ == "__main__":
    # Example usage
    # In a real application, the access_token would come from the OAuth callback
    access_token = "YOUR_ACCESS_TOKEN_HERE"
    profile = fetch_user_profile_claims(access_token)
    if profile:
        import json

        print(json.dumps(profile, indent=2))
