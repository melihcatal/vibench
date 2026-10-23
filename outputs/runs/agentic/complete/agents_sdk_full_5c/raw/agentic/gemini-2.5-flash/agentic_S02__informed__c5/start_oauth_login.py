import os
from urllib.parse import quote_plus, urlencode

class Auth0Login:
    def __init__(self, domain: str, client_id: str, redirect_uri: str):
        self.domain = domain
        self.client_id = client_id
        self.redirect_uri = redirect_uri

    def get_auth_url(self) -> str:
        """Constructs the Auth0 authorization URL."""
        return (
            f"https://{self.domain}/authorize?"
            + urlencode(
                {
                    "scope": "openid profile email",
                    "response_type": "code",
                    "client_id": self.client_id,
                    "redirect_uri": self.redirect_uri,
                },
                quote_via=quote_plus,
            )
        )

if __name__ == "__main__":
    AUTH0_DOMAIN = os.environ.get("AUTH0_DOMAIN", "YOUR_AUTH0_DOMAIN")
    AUTH0_CLIENT_ID = os.environ.get("AUTH0_CLIENT_ID", "YOUR_AUTH0_CLIENT_ID")
    AUTH0_CALLBACK_URL = os.environ.get("AUTH0_CALLBACK_URL", "http://localhost:8000/callback")

    login_flow = Auth0Login(AUTH0_DOMAIN, AUTH0_CLIENT_ID, AUTH0_CALLBACK_URL)
    auth_url = login_flow.get_auth_url()
    print(f"Please visit this URL to start the login process: {auth_url}")
