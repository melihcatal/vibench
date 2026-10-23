import os
from typing import TypedDict
from dotenv import load_dotenv

load_dotenv()

# ---------- Configuration ----------
# Auth0 variables
AUTH0_DOMAIN = os.getenv('AUTH0_DOMAIN')
AUTH0_CLIENT_ID = os.getenv('AUTH0_CLIENT_ID')
AUTH0_CLIENT_SECRET = os.getenv('AUTH0_CLIENT_SECRET')
# Token endpoint used by IdentityClient
TOKEN_ENDPOINT = f'https://{AUTH0_DOMAIN}/oauth/token'

# ---------- IdentityClient ----------
class AuthCodeExchangeRequest(TypedDict):
    grant_type: str
    code: str
    redirect_uri: str
    client_id: str
    client_secret: str

class AuthCodeExchangeResponse(TypedDict):
    access_token: str
    id_token: str
    token_type: str
    expires_in: int
    refresh_token: str

class IdentityClient:
    """Thin wrapper around the Auth0 Management / OAuth token endpoint."""
    def __init__(self, token_url: str = TOKEN_ENDPOINT):
        self.token_url = token_url

    def exchange_code(self, request: AuthCodeExchangeRequest) -> AuthCodeExchangeResponse:
        """Exchange an authorization code for OAuth tokens."""
        payload = {
            'grant_type': request['grant_type'],
            'code': request['code'],
            'redirect_uri': request['redirect_uri'],
            'client_id': request['client_id'],
            'client_secret': request['client_secret']
        }
        resp = requests.post(self.token_url, data=payload)
        resp.raise_for_status()
        return resp.json()

# ---------- Helper utilities ----------

def get_config_value(key: str) -> str:
    value = os.getenv(key)
    if not value:
        raise RuntimeError(f'Missing environment variable: {key}')
    return value

# Example usage (not executed in production code)
if __name__ == '__main__':
    print('Auth0 configured with domain:', AUTH0_DOMAIN)
    print('Client secret redacted:', '*' * 4)

# End of identity_client.py