from identity_client import get_identity_client
from identity_models import normalize_profile_claims


def fetch_profile_claims(id_token, config=None):
    client = get_identity_client(config)
    response = client.get(
        'https://identitytoolkit.googleapis.com/v1/accounts:lookup',
        params={'idToken': id_token, 'key': config['api_key']},
        timeout=30
    )
    response.raise_for_status()
    profile = response.json()
    return normalize_profile_claims(profile)