import os
import requests
from identity_models import UserClaims
import datetime

def fetch_and_normalize_profile_claims(access_token: str, config: dict = None) -> UserClaims:
    config = config or {}
    graph_api_url = config.get('graph_api_url') or os.environ.get('AZURE_AD_GRAPH_API_URL', "https://graph.microsoft.com/v1.0/me")

    headers = {
        'Authorization': f'Bearer {access_token}',
        'Content-Type': 'application/json'
    }

    try:
        response = requests.get(graph_api_url, headers=headers)
        response.raise_for_status()  # Raise an exception for HTTP errors
        raw_claims = response.json()
    except requests.exceptions.RequestException as e:
        raise Exception(f"Failed to fetch user profile from Microsoft Graph API: {e}")

    # Normalize claims from Microsoft Graph API response
    user_claims = UserClaims(
        sub=raw_claims.get('id'), # Azure AD object ID
        name=raw_claims.get('displayName'),
        given_name=raw_claims.get('givenName'),
        family_name=raw_claims.get('surname'),
        preferred_username=raw_claims.get('userPrincipalName'),
        email=raw_claims.get('mail') or raw_claims.get('userPrincipalName'),
        picture=None, # Microsoft Graph /me does not directly return a picture URL by default
        updated_at=datetime.datetime.now(), # Or parse from a relevant Graph API field if available
        raw_claims=raw_claims
    )

    return user_claims
