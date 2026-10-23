import os
import requests
from identity_client import IdentityClient

def start_oauth_login(redirect_uri):
    client = IdentityClient.from_env()
    # Use Auth0 as the OAuth provider
    AUTH0_DOMAIN = client.config['AUTH0_DOMAIN']
    CLIENT_ID = client.config['CLIENT_ID']
    # Request scopes including openid, profile, and email
    scope = 'openid profile email'
    # Generate a random state for CSRF protection
    state = 'state_12345'
    auth_url = (
        f'https://{AUTH0_DOMAIN}/authorize?\n'
        f'response_type=code&\n'
        f'client_id={CLIENT_ID}&\n'
        f'redirect_uri={redirect_uri}&\n'
        f'scope={scope}&\n'
        f'state={state}'
    )
    # Redirect the user agent to the authorization endpoint
    print('Redirect to:', auth_url)
    # In a real web app you would use the framework's redirect function

if __name__ == '__main__':
    start_oauth_login('http://localhost:5000/callback')
