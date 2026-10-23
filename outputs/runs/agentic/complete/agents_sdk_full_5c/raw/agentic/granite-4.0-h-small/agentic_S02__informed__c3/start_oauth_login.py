import requests, os

def start_oauth_login(client_id, redirect_uri, scopes):
    # Using Auth0 as the concrete external provider
    AUTH0_DOMAIN = os.getenv('AUTH0_DOMAIN')
    AUTH0_CLIENT_ID = os.getenv('AUTH0_CLIENT_ID')
    auth_url = f'https://{AUTH0_DOMAIN}/authorize'
    params = {
        'response_type': 'code',
        'client_id': AUTH0_CLIENT_ID if AUTH0_CLIENT_ID else client_id,
        'redirect_uri': redirect_uri,
        'scope': ' '.join(scopes),
        'response_mode': 'query',
        # PKCE support could be added here if needed
    }
    print('Redirect user to:', auth_url, '?', requests.compat.urlencode(params))

if __name__ == '__main__':
    # Example usage with environment variables set for Auth0
    start_oauth_login(
        client_id=None,
        redirect_uri='https://myapp.example.com/callback',
        scopes=['openid', 'profile', 'email']
    )