import os
from authlib.integrations.requests_client import OAuth2Session
from dotenv import load_dotenv


class IdentityClient:
    def __init__(self, provider="Auth0"):
        load_dotenv()
        # Load provider configs
        if provider == "Auth0":
            self.client_id = os.getenv("AUTH0_CLIENT_ID")
            self.client_secret = os.getenv("AUTH0_CLIENT_SECRET")
            self.domain = os.getenv("AUTH0_DOMAIN")
            self.issuer = f"https://{self.domain}"
        elif provider == "Google":
            self.client_id = os.getenv("GOOGLE_CLIENT_ID")
            self.client_secret = os.getenv("GOOGLE_CLIENT_SECRET")
            self.issuer = "https://accounts.google.com"
        else:
            raise ValueError(f"Unsupported provider: {provider}")
        self.provider = provider
        # Authlib session for OAuth2
        self.session = OAuth2Session(
            client_id=self.client_id,
            client_secret=self.client_secret,
            client_kwargs={"scope": "openid profile email"},
        )

    def get_client(self):
        if self.provider == "Auth0":
            self.set_authorize_base_url(f"https://{self.domain}")
        elif self.provider == "Google":
            self.session.authorize_endpoint = (
                "https://accounts.google.com/o/oauth2/v2/auth"
            )
            self.session.token_endpoint = "https://oauth2.googleapis.com/token"
        return self.session

    def set_authorize_base_url(self, base_url):
        self.session.authorize_endpoint = f"{base_url}/authorize"
        self.session.token_endpoint = f"{base_url}/oauth/token"
