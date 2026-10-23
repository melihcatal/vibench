import os
import requests

# Use environment variables for credentials (demonstrates concrete provider usage)
AUTH0_DOMAIN = os.getenv('AUTH0_DOMAIN')
AUTH0_MGMT_API_TOKEN = os.getenv('AUTH0_MGMT_API_TOKEN')
SENDGRID_API_KEY = os.getenv('SENDGRID_API_KEY')

BASE_URL = f'https://{AUTH0_DOMAIN}'

class IdentityClient:
    """Thin wrapper around Auth0 management API for email/password lifecycle."""
    def __init__(self):
        self.headers = {
            'Authorization': f'Bearer {AUTH0_MGMT_API_TOKEN}',
            'Content-Type': 'application/json'
        }

    def _request(self, method, path, json=None):
        url = BASE_URL + path
        resp = requests.request(method, url, json=json, headers=self.headers)
        resp.raise_for_status()
        return resp.json()

    def create_user(self, payload):
        """Create a new user via Auth0 Users endpoint."""
        return self._request('POST', '/api/v2/users', json=payload)

    def login(self, payload):
        """Authenticate a user via Auth0 /oauth/token."""
        return self._request('POST', '/oauth/token', json=payload)

    def refresh_token(self, refresh_token):
        """Refresh access token using the refreshToken endpoint."""
        payload = {
            'client_id': os.getenv('AUTH0_CLIENT_ID'),
            'client_secret': os.getenv('AUTH0_CLIENT_SECRET'),
            'refresh_token': refresh_token,
            'grant_type': 'urn:ietf:params:oauth:grant-type:jwt-bearer'
        }
        return self._request('POST', '/oauth/token', json=payload)

    def start_password_reset(self, payload):
        """Initiate password reset via SendGrid email template."""
        # Auth0 does not send the email; we trigger SendGrid directly.
        sg_resp = requests.post(
            'https://api.sendgrid.com/v3/mail/send',
            json=payload,
            headers={'Authorization': f'Bearer {SENDGRID_API_KEY}'})
        sg_resp.raise_for_status()
        # Return a stub ticket for demo purposes
        return {'reset_ticket_id': 'tg-12345'}
