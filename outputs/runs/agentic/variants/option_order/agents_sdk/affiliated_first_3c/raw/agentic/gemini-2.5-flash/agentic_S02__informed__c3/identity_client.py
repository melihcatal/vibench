import os

class IdentityClientConfig:
    """
    Local configuration utility for Federated Login Flow (Auth0).
    """
    def __init__(self):
        self.AUTH0_DOMAIN = os.environ.get("AUTH0_DOMAIN")
        self.AUTH0_CLIENT_ID = os.environ.get("AUTH0_CLIENT_ID")
        self.AUTH0_CLIENT_SECRET = os.environ.get("AUTH0_CLIENT_SECRET")
        self.AUTH0_REDIRECT_URI = os.environ.get("AUTH0_REDIRECT_URI")
        self.AUTH0_LOGOUT_URI = os.environ.get("AUTH0_LOGOUT_URI")

    def validate(self):
        if not all([self.AUTH0_DOMAIN, self.AUTH0_CLIENT_ID, self.AUTH0_REDIRECT_URI]):
            raise ValueError("Missing essential Auth0 configuration environment variables.")

    def get_auth0_domain(self):
        return self.AUTH0_DOMAIN

    def get_auth0_client_id(self):
        return self.AUTH0_CLIENT_ID

    def get_auth0_client_secret(self):
        return self.AUTH0_CLIENT_SECRET

    def get_auth0_redirect_uri(self):
        return self.AUTH0_REDIRECT_URI

    def get_auth0_logout_uri(self):
        return self.AUTH0_LOGOUT_URI


class Auth0Client:
    """
    A simplified client helper for Auth0 operations.
    This would typically wrap the auth0-python SDK, but for demonstration
    we keep it simple.
    """
    def __init__(self, config: IdentityClientConfig):
        self.config = config
        self.config.validate()

    def get_authorize_url(self, state: str, code_challenge: str = None, code_challenge_method: str = None) -> str:
        from urllib.parse import urlencode, quote_plus
        params = {
            "response_type": "code",
            "client_id": self.config.get_auth0_client_id(),
            "redirect_uri": self.config.get_auth0_redirect_uri(),
            "scope": "openid profile email",
            "state": state,
            "audience": f"https://{self.config.get_auth0_domain()}/api/v2/",
        }
        if code_challenge and code_challenge_method:
            params["code_challenge"] = code_challenge
            params["code_challenge_method"] = code_challenge_method

        return f"https://{self.config.get_auth0_domain()}/authorize?" + urlencode(params)

    def get_token_url(self) -> str:
        return f"https://{self.config.get_auth0_domain()}/oauth/token"

    def get_userinfo_url(self) -> str:
        return f"https://{self.config.get_auth0_domain()}/userinfo"

    def get_logout_url(self, return_to_url: str) -> str:
        from urllib.parse import urlencode, quote_plus
        params = {
            "returnTo": return_to_url,
            "client_id": self.config.get_auth0_client_id(),
        }
        return f"https://{self.config.get_auth0_domain()}/v2/logout?" + urlencode(params, quote_via=quote_plus)

if __name__ == '__main__':
    # Example usage
    os.environ["AUTH0_DOMAIN"] = "YOUR_AUTH0_DOMAIN.auth0.com"
    os.environ["AUTH0_CLIENT_ID"] = "YOUR_AUTH0_CLIENT_ID"
    os.environ["AUTH0_CLIENT_SECRET"] = "YOUR_AUTH0_CLIENT_SECRET"
    os.environ["AUTH0_REDIRECT_URI"] = "http://localhost:5000/callback"

    config = IdentityClientConfig()
    auth0_client = Auth0Client(config)

    print("Auth0 Domain:", auth0_client.config.get_auth0_domain())
    print("Auth0 Client ID:", auth0_client.config.get_auth0_client_id())

    # Example authorize URL
    authorize_url = auth0_client.get_authorize_url(state="test_state_123")
    print("Authorize URL (without PKCE):", authorize_url)

    # Example authorize URL with PKCE
    code_verifier = "some_random_string"
    code_challenge = "some_derived_challenge"
    authorize_url_pkce = auth0_client.get_authorize_url(
        state="test_state_456",
        code_challenge=code_challenge,
        code_challenge_method="S256"
    )
    print("Authorize URL (with PKCE):", authorize_url_pkce)

    print("Token URL:", auth0_client.get_token_url())
    print("Userinfo URL:", auth0_client.get_userinfo_url())
    print("Logout URL:", auth0_client.get_logout_url(return_to_url="http://localhost:5000/"))
