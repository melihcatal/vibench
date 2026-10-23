import os, requests

class IdentityClient:
    def __init__(self):
        # Azure AD B2C tenant and application settings
        self.tenant_id = os.getenv('TENANT_ID')
        self.client_id = os.getenv('CLIENT_ID')
        self.client_secret = os.getenv('CLIENT_SECRET')
        self.authority = f'https://{self.tenant_id}.b2clogin.com/{self.tenant_id}/v2.0/'

    def call_api(self, method, path, json=None, data=None, headers=None):
        # Construct full URL
        url = f'{self.authority}{path}'
        # Obtain an access token for Management API calls (could also be user token)
        token = self.get_access_token()
        headers = headers or {}
        headers['Authorization'] = f'Bearer {token}'
        # Perform request
        response = requests.request(method, url, json=json, data=data, headers=headers)
        return response

    def get_access_token(self):
        token_url = f'{self.authority}oauth2/v2.0/token'
        payload = {
            'grant_type': 'client_credentials',
            'scope': 'https://<tenant>.onmicrosoft.com/<app_id>/user_impersonation',
            'client_id': self.client_id,
            'client_secret': self.client_secret
        }
        resp = requests.post(token_url, data=payload)
        resp.raise_for_status()
        return resp.json()['access_token']
