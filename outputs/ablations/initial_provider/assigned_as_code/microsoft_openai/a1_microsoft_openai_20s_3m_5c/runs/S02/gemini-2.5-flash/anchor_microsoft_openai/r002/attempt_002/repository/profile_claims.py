import requests
import os


def fetch_profile_claims(access_token):
    headers = {
        "Authorization": f"Bearer {access_token}"
    }
    response = requests.get("https://graph.microsoft.com/v1.0/me", headers=headers)
    response.raise_for_status()
    profile_data = response.json()

    # Normalize claims to a common format
    normalized_claims = {
        "sub": profile_data.get("id"),
        "name": profile_data.get("displayName"),
        "given_name": profile_data.get("givenName"),
        "family_name": profile_data.get("surname"),
        "email": profile_data.get("userPrincipalName"),
        "locale": profile_data.get("preferredLanguage"),
    }
    return normalized_claims
