import os
from auth0.management import Auth0
from auth0.authentication import Auth0Authentication


class IdentityClient:
    def __init__(self, domain: str, client_id: str, client_secret: str, redirect_uri: str):
        self.domain = domain
        self.client_id = client_id
        self.client_secret = client_secret
        self.redirect_uri = redirect_uri
        self.auth0_authentication = Auth0Authentication(domain, client_id, client_secret)
        # Note: Auth0 Management API requires a Management API Access Token
        # For simpler flows like login, Auth0Authentication is usually sufficient.
        # If Management API calls are needed, an additional token retrieval step would be required.

    def get_auth_url(self, scope: str, state: str, audience: str = None, code_challenge: str = None, code_challenge_method: str = None):
        params = {
            "client_id": self.client_id,
            "response_type": "code",
            "redirect_uri": self.redirect_uri,
            "scope": scope,
            "state": state,
        }
        if audience:
            params["audience"] = audience
        if code_challenge and code_challenge_method:
            params["code_challenge"] = code_challenge
            params["code_challenge_method"] = code_challenge_method

        query_string = "&".join([f"{k}={v}" for k, v in params.items()])
        return f"https://{self.domain}/authorize?{query_string}"

    def exchange_code_for_tokens(self, code: str, redirect_uri: str, code_verifier: str = None):
        payload = {
            "client_id": self.client_id,
            "client_secret": self.client_secret,
            "code": code,
            "redirect_uri": redirect_uri,
            "grant_type": "authorization_code",
        }
        if code_verifier:
            payload["code_verifier"] = code_verifier

        return self.auth0_authentication.oauth_token(payload=payload)

    def get_userinfo(self, access_token: str):
        return self.auth0_authentication.userinfo(access_token)


def get_identity_client():
    domain = os.environ.get("AUTH0_DOMAIN")
    client_id = os.environ.get("AUTH0_CLIENT_ID")
    client_secret = os.environ.get("AUTH0_CLIENT_SECRET")
    redirect_uri = os.environ.get("AUTH0_CALLBACK_URL")

    if not all([domain, client_id, client_secret, redirect_uri]):
        raise ValueError("AUTH0_DOMAIN, AUTH0_CLIENT_ID, AUTH0_CLIENT_SECRET, and AUTH0_CALLBACK_URL must be set as environment variables.")

    return IdentityClient(domain, client_id, client_secret, redirect_uri)
