import os
from typing import Any, Dict, Optional

import requests


class Auth0IdentityClient:
    def __init__(
        self,
        domain: Optional[str] = None,
        client_id: Optional[str] = None,
        client_secret: Optional[str] = None,
    ):
        self.domain = domain or os.environ.get("AUTH0_DOMAIN")
        self.client_id = client_id or os.environ.get("AUTH0_CLIENT_ID")
        self.client_secret = client_secret or os.environ.get("AUTH0_CLIENT_SECRET")

    @property
    def issuer(self) -> str:
        return f"https://{self.domain}/"

    @property
    def authorize_endpoint(self) -> str:
        return f"https://{self.domain}/authorize"

    @property
    def token_endpoint(self) -> str:
        return f"https://{self.domain}/oauth/token"

    @property
    def userinfo_endpoint(self) -> str:
        return f"https://{self.domain}/userinfo"

    def build_authorize_url(
        self,
        redirect_uri: str,
        state: str,
        nonce: str,
        scope: str = "openid profile email",
        code_challenge: Optional[str] = None,
        prompt: Optional[str] = None,
    ) -> str:
        params: Dict[str, Any] = {
            "client_id": self.client_id,
            "response_type": "code",
            "redirect_uri": redirect_uri,
            "scope": scope,
            "state": state,
            "nonce": nonce,
        }
        if code_challenge:
            params["code_challenge"] = code_challenge
            params["code_challenge_method"] = "S256"
        if prompt:
            params["prompt"] = prompt
        return (
            requests.Request("GET", self.authorize_endpoint, params=params)
            .prepare()
            .url
        )

    def exchange_code(
        self, code: str, redirect_uri: str, code_verifier: Optional[str] = None
    ) -> Dict[str, Any]:
        payload = {
            "grant_type": "authorization_code",
            "client_id": self.client_id,
            "client_secret": self.client_secret,
            "code": code,
            "redirect_uri": redirect_uri,
        }
        if code_verifier:
            payload["code_verifier"] = code_verifier
        response = requests.post(self.token_endpoint, json=payload, timeout=30)
        response.raise_for_status()
        return response.json()

    def fetch_profile(self, access_token: str) -> Dict[str, Any]:
        response = requests.get(
            self.userinfo_endpoint,
            headers={"Authorization": f"Bearer {access_token}"},
            timeout=30,
        )
        response.raise_for_status()
        return response.json()


def load_identity_client() -> Auth0IdentityClient:
    return Auth0IdentityClient()
