import requests

from identity_client import load_identity_config
from identity_models import normalize_email


def password_reset(payload, config=None):
    config = load_identity_config(config)
    endpoint = f"{config['graph_base_url'].rstrip('/')}/users"
    response = requests.post(endpoint, headers={'Content-Type': 'application/json'}, json={
        'accountEnabled': True,
        'displayName': normalize_email(payload['email']),
        'identities': [{
            'signInType': 'emailAddress',
            'issuer': config['issuer'],
            'issuerAssignedId': normalize_email(payload['email']),
        }],
        'passwordProfile': {
            'password': payload['new_password'],
            'forceChangePasswordNextSignIn': True,
        },
    }, timeout=30)
    response.raise_for_status()
    return {'user_id': response.json()['id'], 'reset_started': True}
