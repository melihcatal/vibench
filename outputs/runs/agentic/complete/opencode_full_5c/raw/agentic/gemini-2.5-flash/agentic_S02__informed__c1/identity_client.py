import os
from urllib.parse import urlencode, urljoin
from typing import Dict, Any


class IdentityClient:
    def __init__(self):
        self.auth0_domain = os.environ.get("AUTH0_DOMAIN")
        self.auth0_client_id = os.environ.get("AUTH0_CLIENT_ID")
        self.auth0_client_secret = os.environ.get("AUTH0_CLIENT_SECRET")
        self.redirect_uri = os.environ.get(
            "AUTH0_REDIRECT_URI", "http://localhost:8080/callback"
        )
        if not self.auth0_domain or not self.auth0_client_id:
            raise ValueError(
                "AUTH0_DOMAIN and AUTH0_CLIENT_ID must be set in environment variables."
            )

    def get_authorize_url(
        self,
        scope: str,
        state: str,
        code_challenge: str = None,
        code_challenge_method: str = None,
    ) -> str:
        params = {
            "response_type": "code",
            "client_id": self.auth0_client_id,
            "redirect_uri": self.redirect_uri,
            "scope": scope,
            "state": state,
        }
        if code_challenge and code_challenge_method:
            params["code_challenge"] = code_challenge
            params["code_challenge_method"] = code_challenge_method
        return (
            urljoin(f"https://{self.auth0_domain}", "/authorize")
            + "?"
            + urlencode(params)
        )

    def get_token_url(self) -> str:
        return urljoin(f"https://{self.auth0_domain}", "/oauth/token")

    def get_userinfo_url(self) -> str:
        return urljoin(f"https://{self.auth0_domain}", "/userinfo")

    def get_audience(self) -> str:
        # For Auth0, typically the audience is the API Identifier.
        # This can be configured as an environment variable if needed.
        return os.environ.get(
            "AUTH0_API_AUDIENCE", f"https://{self.auth0_domain}/api/v2/"
        )
