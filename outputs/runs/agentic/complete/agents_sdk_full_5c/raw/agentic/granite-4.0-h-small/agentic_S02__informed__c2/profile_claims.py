import os
import json
import requests

# Provider: Microsoft Entra OIDC\n# SDK/REST: Direct Graph API call using access token obtained from oauth_callback.py\n
# Configuration (environment variables)\nTENANT_ID = os.getenv('AZURE_TENANT_ID')
CLIENT_ID = os.getenv('AZURE_CLIENT_ID')\n# The access token is expected to be provided as an argument; in a real app it would be stored securely after callback\nACCESS_TOKEN = os.getenv('ACCESS_TOKEN')  # for simplicity; production: encrypted store\n
# Microsoft Graph endpoint for the user profile\nGRAPH_ME_ENDPOINT = f'https://graph.microsoft.com/v1.0/me'

def fetch_profile(access_token: str) -> dict:
    """Call Microsoft Graph Me endpoint and return the raw JSON payload containing federated profile claims."""
    headers = {
        'Authorization': f'Bearer {access_token}',
        'Accept': 'application/json'
    }
    response = requests.get(GRAPH_ME_ENDPOINT, headers=headers, timeout=10)
    response.raise_for_status()
    return response.json()

# Example normalization function that maps Graph claims to a common internal model\ndef normalize_claims(raw_claims: dict) -> dict:
    normalized = {
        # Basic identity\n        'sub': raw_claims.get('id'),                       # subject identifier\n        'name': raw_claims.get('displayName'),             # full name\n        'given_name': raw_claims.get('givenName'),         # first name\n        'family_name': raw_claims.get('surname'),          # last name\n        'email': raw_claims.get('mail') or raw_claims.get('userPrincipalName'),  # preferred email\n        'preferred_username': raw_claims.get('userPrincipalName'),
        'locale': raw_claims.get('locale'),                # language tag\n        # Optional supplemental data\n        'phone_numbers': raw_claims.get('telephoneNumber'),
        'job_title': raw_claims.get('jobTitle'),
        'department': raw_claims.get('department'),
        'company_name': raw_claims.get('companyName'),
        # Provider-specific identifiers (useful for auditing)\n        'provider': 'microsoft_azure',
        'provider_user_id': raw_claims.get('objectId')
    }
    return normalized

# Simple wrapper that orchestrates fetch and normalization\ndef get_profile_claims() -> dict:
    raw = fetch_profile(ACCESS_TOKEN)
    return normalize_claims(raw)

# ------------------------------------------------------------------------------\n# Example usage (for local testing only, remove or protect in production)\nif __name__ == '__main__':
    if not ACCESS_TOKEN:
        raise RuntimeError('Set ACCESS_TOKEN environment variable with a valid token before running')
    claims = get_profile_claims()
    print(json.dumps(claims, indent=2))
