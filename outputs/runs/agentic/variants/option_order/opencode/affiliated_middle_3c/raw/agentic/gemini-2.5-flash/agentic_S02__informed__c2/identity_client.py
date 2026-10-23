import os
from auth0.management import Auth0
from auth0.authentication import Auth0Authentication
from urllib.parse import urlencode


class Auth0Client:
    def __init__(self):
        self.domain = os.environ.get("AUTH0_DOMAIN")
        self.client_id = os.environ.get("AUTH0_CLIENT_ID")
        self.client_secret = os.environ.get("AUTH0_CLIENT_SECRET")
        if not all([self.domain, self.client_id]):
            raise ValueError(
                "AUTH0_DOMAIN and AUTH0_CLIENT_ID environment variables must be set."
            )
        self.auth0_authentication = Auth0Authentication(self.domain, self.client_id)

    def get_authorize_url(
        self,
        redirect_uri: str,
        scope: str,
        audience: Optional[str] = None,
        state: Optional[str] = None,
        response_type: str = "code",
        code_challenge: Optional[str] = None,
        code_challenge_method: Optional[str] = None,
    ):
        params = {
            "response_type": response_type,
            "client_id": self.client_id,
            "redirect_uri": redirect_uri,
            "scope": scope,
            "state": state,
        }
        if audience:
            params["audience"] = audience
        if code_challenge and code_challenge_method:
            params["code_challenge"] = code_challenge
            params["code_challenge_method"] = code_challenge_method
        return f"https://{self.domain}/authorize?{urlencode(params)}"

    def exchange_code_for_tokens(
        self, code: str, redirect_uri: str, code_verifier: Optional[str] = None
    ):
        if not self.client_secret and not code_verifier:
            raise ValueError(
                "AUTH0_CLIENT_SECRET or code_verifier must be provided for token exchange."
            )
        data = {
            "grant_type": "authorization_code",
            "client_id": self.client_id,
            "code": code,
            "redirect_uri": redirect_uri,
        }
        if self.client_secret:
            data["client_secret"] = self.client_secret
        if code_verifier:
            data["code_verifier"] = code_verifier

        return self.auth0_authentication.oauth_token(data)

    def get_userinfo(self, access_token: str):
        return self.auth0_authentication.userinfo(access_token)
