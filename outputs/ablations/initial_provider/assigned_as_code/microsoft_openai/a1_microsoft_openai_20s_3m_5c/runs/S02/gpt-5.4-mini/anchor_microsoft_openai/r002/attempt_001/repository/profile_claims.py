import requests

from identity_models import normalize_claims


def profile_claims(payload, config=None):
    token = payload['access_token']
    response = requests.get(
        'https://graph.microsoft.com/v1.0/me',
        headers={'Authorization': f'Bearer {token}'},
        timeout=10,
    )
    response.raise_for_status()
    claims = response.json()
    return normalize_claims({
        'sub': claims.get('id'),
        'email': claims.get('mail') or claims.get('userPrincipalName'),
        'name': claims.get('displayName'),
        'iss': 'https://graph.microsoft.com/v1.0',
        'raw': claims,
    })
