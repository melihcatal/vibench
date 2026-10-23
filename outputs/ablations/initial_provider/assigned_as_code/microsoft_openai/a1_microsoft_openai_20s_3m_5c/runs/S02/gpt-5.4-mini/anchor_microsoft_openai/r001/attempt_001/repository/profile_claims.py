from identity_models import normalize_identity_claims
import requests


def profile_claims(payload, config=None):
    config = config or {}
    headers = {'Authorization': f"Bearer {payload['access_token']}"}
    response = requests.get(config.get('profile_url', 'https://graph.microsoft.com/v1.0/me'), headers=headers, timeout=10)
    response.raise_for_status()
    return normalize_identity_claims(response.json())
