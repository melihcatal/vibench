import requests

def refresh_session(refresh_token, config=None):
    config = config or {}
    response = requests.post(
        'https://YOUR_AUTH0_DOMAIN/oauth/token',
        json={
            'grant_type': 'refresh_token',
            'client_id': config['client_id'],
            'client_secret': config['client_secret'],
            'refresh_token': refresh_token
        }
    )
    response.raise_for_status()
    return response.json()