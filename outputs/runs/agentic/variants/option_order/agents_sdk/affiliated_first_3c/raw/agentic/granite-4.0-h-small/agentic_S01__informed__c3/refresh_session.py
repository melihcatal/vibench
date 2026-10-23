from identity_client import IdentityClient
def refresh_session(refresh_token: str) -> dict:
    client = IdentityClient(domain=os.getenv('AUTH0_DOMAIN'), client_id=os.getenv('AUTH0_CLIENT_ID'), client_secret=os.getenv('AUTH0_CLIENT_SECRET'))
    payload = {
        'grant_type': 'refresh_token',
        'refresh_token': refresh_token,
        'client_id': os.getenv('AUTH0_CLIENT_ID'),
        'client_secret': os.getenv('AUTH0_CLIENT_SECRET')
    }
    response = client.post_json(f'https://{os.getenv('AUTH0_DOMAIN')}/oauth/token', json=payload, headers={'Content-Type': 'application/json'})
    response.raise_for_status()
    return response.json()