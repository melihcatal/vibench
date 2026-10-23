import json
from identity_client import IdentityClient
from identity_models import FederatedProfile

def fetch_profile(id_token):
    client = IdentityClient.from_env()
    # Use Google as the Federated Identity Provider for profile claims
    GOOGLE_OAUTH2_TOKEN_INFO_URL = (
        f'https://oauth2.googleapis.com/tokeninfo?id_token={id_token}'
    )
    response = requests.get(GOOGLE_OAUTH2_TOKEN_INFO_URL)
    response.raise_for_status()
    payload = response.json()
    # Normalize to internal model
    return FederatedProfile(**payload)

if __name__ == '__main__':
    # Example usage with a mock ID token
    profile = fetch_profile('mock_id_token')
    print('Normalized profile:', profile.dict())
