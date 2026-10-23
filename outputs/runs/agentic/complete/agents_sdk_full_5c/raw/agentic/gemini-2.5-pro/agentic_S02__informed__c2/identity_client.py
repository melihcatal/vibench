import os
from auth0.authentication import GetToken, UserInfo
from auth0.management import Auth0

class Auth0Client:
    def __init__(self):
        self.domain = os.environ.get("AUTH0_DOMAIN")
        self.client_id = os.environ.get("AUTH0_CLIENT_ID")
        self.client_secret = os.environ.get("AUTH0_CLIENT_SECRET")
        self.redirect_uri = f"{os.environ.get('APP_BASE_URL', 'http://localhost:3000')}/callback"
        
        if not all([self.domain, self.client_id]):
            raise ValueError("AUTH0_DOMAIN and AUTH0_CLIENT_ID must be set.")

        self.get_token = GetToken(self.domain, self.client_id, self.client_secret)
        self.userinfo = UserInfo(self.domain).userinfo
        self._mgmt_client = None

    @property
    def mgmt(self):
        """Lazy initializer for the Management API client."""
        if self._mgmt_client is None:
            if not self.client_secret:
                 raise ValueError("AUTH0_CLIENT_SECRET is required for Management API.")
            
            # For machine-to-machine communication with the Management API
            get_token = GetToken(self.domain, self.client_id, self.client_secret)
            token_info = get_token.client_credentials(f'https://{self.domain}/api/v2/')
            mgmt_token = token_info['access_token']
            self._mgmt_client = Auth0(self.domain, mgmt_token)
        return self._mgmt_client


_auth0_client_instance = None

def get_auth0_client() -> Auth0Client:
    """Provides a singleton instance of the Auth0Client."""
    global _auth0_client_instance
    if _auth0_client_instance is None:
        _auth0_client_instance = Auth0Client()
    return _auth0_client_instance
