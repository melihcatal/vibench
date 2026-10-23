
import os
import requests

class FederatedLoginConfig:
    """
    Provides local configuration for the Federated Login Flow.
    """
    def __init__(self):
        self.authority = os.environ.get("FEDERATED_AUTHORITY", "https://example.com/oauth2")
        self.client_id = os.environ.get("FEDERATED_CLIENT_ID", "your_client_id")
        self.client_secret = os.environ.get("FEDERATED_CLIENT_SECRET", None)
        self.redirect_uri = os.environ.get("FEDERATED_REDIRECT_URI", "http://localhost:8080/callback")
        self.scope = os.environ.get("FEDERATED_SCOPE", "openid profile email")
        self.response_type = "code"
        self.grant_type = "authorization_code"

class FederatedLoginClient:
    """
    Provides client helper utilities for the Federated Login Flow.
    """
    def __init__(self, config: FederatedLoginConfig):
        self.config = config

    def get_authorization_url(self, state: str, code_challenge: str = None, code_challenge_method: str = None) -> str:
        """
        Constructs the authorization URL.
        """
        params = {
            "client_id": self.config.client_id,
            "redirect_uri": self.config.redirect_uri,
            "response_type": self.config.response_type,
            "scope": self.config.scope,
            "state": state,
        }
        if code_challenge and code_challenge_method:
            params["code_challenge"] = code_challenge
            params["code_challenge_method"] = code_challenge_method

        query_string = "&".join(f"{key}={value}" for key, value in params.items())
        return f"{self.config.authority}/authorize?{query_string}"

    def exchange_code_for_tokens(self, code: str, code_verifier: str = None) -> dict:
        """
        Exchanges the authorization code for tokens.
        """
        token_endpoint = f"{self.config.authority}/token"
        headers = {"Content-Type": "application/x-www-form-urlencoded"}
        data = {
            "grant_type": self.config.grant_type,
            "client_id": self.config.client_id,
            "redirect_uri": self.config.redirect_uri,
            "code": code,
        }
        if self.config.client_secret:
            data["client_secret"] = self.config.client_secret
        if code_verifier:
            data["code_verifier"] = code_verifier

        response = requests.post(token_endpoint, headers=headers, data=data)
        response.raise_for_status()
        return response.json()

    def get_user_info(self, access_token: str) -> dict:
        """
        Fetches user information using the access token.
        """
        userinfo_endpoint = f"{self.config.authority}/userinfo"
        headers = {"Authorization": f"Bearer {access_token}"}
        response = requests.get(userinfo_endpoint, headers=headers)
        response.raise_for_status()
        return response.json()
