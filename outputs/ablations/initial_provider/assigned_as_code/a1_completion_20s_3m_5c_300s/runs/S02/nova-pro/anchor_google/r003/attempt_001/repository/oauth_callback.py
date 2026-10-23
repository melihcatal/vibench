import requests

from identity_client import get_identity_client


def handle_oauth_callback(code, config=None):
    client = get_identity_client(config)
    response = client.post(
        'https://identitytoolkit.googleapis.com/v1/accounts:exchangeAuthCode',
        json={'code': code, 'clientId': config['client_id']},
        params={'key': config['api_key']},
        timeout=30
    )
    response.raise_for_status()
    return response.json()