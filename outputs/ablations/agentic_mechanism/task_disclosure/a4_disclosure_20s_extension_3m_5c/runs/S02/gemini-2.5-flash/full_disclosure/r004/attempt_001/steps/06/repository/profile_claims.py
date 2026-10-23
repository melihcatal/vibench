import requests
import os

GOOGLE_USERINFO_URL = "https://openidconnect.googleapis.com/v1/userinfo"

def fetch_google_profile_claims(access_token: str) -> dict:
    """
    Fetches user profile claims from Google's OpenID Connect UserInfo endpoint.
    """
    headers = {
        "Authorization": f"Bearer {access_token}"
    }
    response = requests.get(GOOGLE_USERINFO_URL, headers=headers)
    response.raise_for_status()
    return response.json()

def normalize_claims(claims: dict) -> dict:
    """
    Normalizes a dictionary of claims into a consistent format.
    This example provides basic normalization for Google claims.
    """
    normalized = {
        "sub": claims.get("sub"),
        "email": claims.get("email"),
        "email_verified": claims.get("email_verified"),
        "name": claims.get("name"),
        "given_name": claims.get("given_name"),
        "family_name": claims.get("family_name"),
        "picture": claims.get("picture"),
        "locale": claims.get("locale"),
        # Add other claims as needed, mapping them to a common schema
    }
    return {k: v for k, v in normalized.items() if v is not None}
