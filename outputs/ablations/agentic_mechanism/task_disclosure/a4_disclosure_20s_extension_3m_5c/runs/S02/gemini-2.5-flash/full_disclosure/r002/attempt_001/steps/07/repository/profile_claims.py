
import requests
import os

AUTH0_DOMAIN = os.environ.get("AUTH0_DOMAIN")
AUTH0_CLIENT_ID = os.environ.get("AUTH0_CLIENT_ID")

def fetch_and_normalize_profile_claims(access_token: str) -> dict:
    """
    Fetches user profile claims from Auth0 and normalizes them.

    Args:
        access_token: The access token obtained during the login flow.

    Returns:
        A dictionary containing the normalized user profile claims.
    """
    if not AUTH0_DOMAIN:
        raise ValueError("AUTH0_DOMAIN environment variable not set.")

    userinfo_url = f"https://{AUTH0_DOMAIN}/userinfo"
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }

    response = requests.get(userinfo_url, headers=headers)
    response.raise_for_status()  # Raise an exception for HTTP errors

    claims = response.json()

    # Normalize claims (example: mapping Auth0 claims to a generic format)
    normalized_claims = {
        "sub": claims.get("sub"),
        "name": claims.get("name"),
        "email": claims.get("email"),
        "picture": claims.get("picture"),
        "email_verified": claims.get("email_verified"),
        "federated_provider": claims.get("identities", [{}])[0].get("provider") if claims.get("identities") else None
    }
    return normalized_claims

