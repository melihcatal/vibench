import os
import requests

class IdentityClient:
    """
    Helper client for Auth0 authentication flows.
    Uses environment variables for concrete configuration.
    """
    AUTH0_DOMAIN = os.getenv('AUTH0_DOMAIN')
    AUTH0_CLIENT_ID = os.getenv('AUTH0_CLIENT_ID')
    AUTH0_CLIENT_SECRET = os.getenv('AUTH0_CLIENT_SECRET')
    AUTH0_MGMT_API_TOKEN = os.getenv('AUTH0_MGMT_API_TOKEN')

    def __init__(self):
        if not self.AUTH0_DOMAIN or not self.AUTH0_CLIENT_ID:
            raise RuntimeError('Auth0 configuration missing (AUTH0_DOMAIN, AUTH0_CLIENT_ID)')

    def build_authorize_url(self, redirect_uri, scopes, state, pkce=False):
        params = {
            'response_type': 'code',
            'client_id': self.AUTH0_CLIENT_ID,
            'redirect_uri': redirect_uri,
            'scope': ' '.join(scopes),
            'state': state,
        }
        if pkce:
            params['response_mode'] = 'query'
        return f'https://{self.AUTH0_DOMAIN}/authorize?' + requests.compat.urlencode(params)

    def exchange_code(self, auth_code, redirect_uri):
        """Exchange an authorization code for tokens using the Auth0 token endpoint."""
        token_url = f'https://{self.AUTH0_DOMAIN}/oauth/token'
        payload = {
            'grant_type': 'authorization_code',
            'code': auth_code,
            'redirect_uri': redirect_uri,
            'client_id': self.AUTH0_CLIENT_ID,
            'client_secret': self.AUTH0_CLIENT_SECRET,
        }
        resp = requests.post(token_url, data=payload, timeout=10)
        resp.raise_for_status()
        return resp.json()

    def get_userinfo(self, access_token):
        """Fetch profile information from Auth0 /userinfo endpoint."""
        url = f'https://{self.AUTH0_DOMAIN}/userinfo'
        headers = {'Authorization': f'Bearer {access_token}'}
        resp = requests.get(url, headers=headers, timeout=10)
        resp.raise_for_status()
        return resp.json()

    def fetch_management_user(self, user_id):
        """Retrieve user details from Auth0 Management API."""
        url = f'https://{self.AUTH0_DOMAIN}/api/v2/users/{user_id}'
        headers = {
            'Authorization': f'Bearer {self.AUTH0_MGMT_API_TOKEN}'
        }
        resp = requests.get(url, headers=headers, timeout=10)
        resp.raise_for_status()
        return resp.json()

if __name__ == '__main__':
    # Example usage (env vars must be set)
    client = IdentityClient()
    print('Auth URL:', client.build_authorize_url('https://myapp.com/callback', ['openid', 'profile'], 'my-state'))
