import os, requests, json

def exchange_code_for_token(auth_code, redirect_uri, client_id=None, client_secret=None):
    # Concrete provider: Auth0 Authentication API
    AUTH0_DOMAIN = os.getenv('AUTH0_DOMAIN')
    AUTH0_CLIENT_ID = os.getenv('AUTH0_CLIENT_ID')
    AUTH0_CLIENT_SECRET = os.getenv('AUTH0_CLIENT_SECRET')

    token_url = f'https://{AUTH0_DOMAIN}/oauth/token'
    payload = {
        'grant_type': 'authorization_code',
        'code': auth_code,
        'redirect_uri': redirect_uri,
        'client_id': AUTH0_CLIENT_ID if AUTH0_CLIENT_ID else client_id,
        'client_secret': AUTH0_CLIENT_SECRET if AUTH0_CLIENT_SECRET else client_secret,
    }
    response = requests.post(token_url, data=payload, timeout=10)
    response.raise_for_status()
    return response.json()

if __name__ == '__main__':
    # Example usage (environment variables AUTH0_* must be defined)
    auth_code = 'AUTHORIZATION_CODE_FROM_CALLBACK'
    redirect_uri = 'https://myapp.example.com/callback'
    token_data = exchange_code_for_token(auth_code, redirect_uri)
    print('Access token:', token_data.get('access_token'))
    print('ID token:', token_data.get('id_token'))