import os
import urllib.parse
import base64
import hashlib
import secrets
from typing import Dict, Any
import requests

from identity_models import Auth0TokenResponse


class Auth0Client:
    def __init__(self):
        self.domain = os.environ.get("AUTH0_DOMAIN")
        self.client_id = os.environ.get("AUTH0_CLIENT_ID")
        self.client_secret = os.environ.get("AUTH0_CLIENT_SECRET")
        self.redirect_uri = os.environ.get("AUTH0_REDIRECT_URI")
        if not all([self.domain, self.client_id, self.redirect_uri]):
            raise ValueError(
                "AUTH0_DOMAIN, AUTH0_CLIENT_ID, and AUTH0_REDIRECT_URI must be set as environment variables."
            )

    def get_authorization_url(
        self, scope: str = "openid profile email", state: str = None
    ) -> str:
        params = {
            "response_type": "code",
            "client_id": self.client_id,
            "redirect_uri": self.redirect_uri,
            "scope": scope,
            "audience": f"https://{self.domain}/api/v2/",
        }
        if state:
            params["state"] = state
        return f"https://{self.domain}/authorize?{urllib.parse.urlencode(params)}"

    def exchange_code_for_tokens(
        self, code: str, code_verifier: str = None
    ) -> Auth0TokenResponse:
        headers = {"Content-Type": "application/x-www-form-urlencoded"}
        data = {
            "grant_type": "authorization_code",
            "client_id": self.client_id,
            "client_secret": self.client_secret,
            "code": code,
            "redirect_uri": self.redirect_uri,
        }
        if code_verifier:
            data["code_verifier"] = code_verifier

        response = requests.post(
            f"https://{self.domain}/oauth/token", headers=headers, data=data
        )
        response.raise_for_status()
        return Auth0TokenResponse(**response.json())

    def get_userinfo(self, access_token: str) -> Dict[str, Any]:
        headers = {"Authorization": f"Bearer {access_token}"}
        response = requests.get(f"https://{self.domain}/userinfo", headers=headers)
        response.raise_for_status()
        return response.json()

    @staticmethod
    def generate_pkce_challenge() -> Dict[str, str]:
        code_verifier = secrets.token_urlsafe(64)
        code_challenge = (
            base64.urlsafe_b64encode(
                hashlib.sha256(code_verifier.encode("utf-8")).digest()
            )
            .decode("utf-8")
            .replace("=", "")
        )
        return {"code_verifier": code_verifier, "code_challenge": code_challenge}

    def get_pkce_authorization_url(
        self,
        code_challenge: str,
        scope: str = "openid profile email",
        state: str = None,
    ) -> str:
        params = {
            "response_type": "code",
            "client_id": self.client_id,
            "redirect_uri": self.redirect_uri,
            "scope": scope,
            "code_challenge": code_challenge,
            "code_challenge_method": "S256",
            "audience": f"https://{self.domain}/api/v2/",
        }
        if state:
            params["state"] = state
        return f"https://{self.domain}/authorize?{urllib.parse.urlencode(params)}"
