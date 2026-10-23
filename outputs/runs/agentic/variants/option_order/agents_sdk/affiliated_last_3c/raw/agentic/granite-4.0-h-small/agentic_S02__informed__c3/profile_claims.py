import os
import requests
from identity_models import FederatedProfile

# Configurable values – set env vars or replace with constants
AUTH0_DOMAIN = os.getenv('AUTH0_DOMAIN', 'your-auth0-domain.auth0.com')
API_AUDIENCE = os.getenv('API_AUDIENCE', 'https://your-api/audience')
# Assuming Auth0 Management API token stored in env var MANAGEMENT_TOKEN
MANAGEMENT_TOKEN = os.getenv('AUTH0_MGMT_TOKEN')

BASE_URL = f'https://{AUTH0_DOMAIN}"

headers = {
    'Authorization': f'Bearer {MANAGEMENT_TOKEN}',
    'Content-Type': 'application/json',
}

def fetch_user_profile(access_token: str) -> FederatedProfile:
    """
    Exchange an access token (obtained from OIDC login) for Auth0 user metadata.
    Returns a normalized FederatedProfile instance.
    """
    token_info_url = f"{BASE_URL}/userinfo"
    resp = requests.get(token_info_url, headers={'Authorization': f'Bearer {access_token}'})
    resp.raise_for_status()
    user_data = resp.json()
    # Normalization – map Auth0 fields to a generic profile schema
    profile = {
        'sub': user_data.get('sub'),  # unique identifier
        'email': user_data.get('email'),
        'email_verified': user_data.get('email_verified'),
        'name': user_data.get('name'),
        'given_name': user_data.get('given_name'),
        'family_name': user_data.get('family_name'),
        'nickname': user_data.get('nickname'),
        'picture': user_data.get('picture'),
        # Add any custom claims here
    }
    return FederatedProfile(**profile)

# Example usage (could be called from a web view or another service)
if __name__ == '__main__':
    # In real app you'd receive the token from the callback handler
    demo_access_token = os.getenv('DEMO_ACCESS_TOKEN')
    if demo_access_token:
        profile = fetch_user_profile(demo_access_token)
        print('Normalized profile:', profile.dict())
    else:
        print('Set DEMO_ACCESS_TOKEN env var to test.')
