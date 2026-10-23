import os
import base64
import hashlib
import requests
from typing import Dict, Any, Optional
from urllib.parse import urlencode


class IdentityClient:
    GOOGLE_OAUTH_AUTH_URL = "https://accounts.google.com/o/oauth2/v2/auth"
    GOOGLE_OAUTH_TOKEN_URL = "https://oauth2.googleapis.com/token"
    GOOGLE_USERINFO_URL = "https://openidconnect.googleapis.com/v1/userinfo"

    def __init__(self, client_id: str, client_secret: str, redirect_uri: str):
        self.client_id = client_id
        self.client_secret = client_secret
        self.redirect_uri = redirect_uri

    def get_authorization_url(self, scopes: list, state: str, code_challenge: Optional[str] = None) -> str:
        params = {
            "client_id": self.client_id,
            "redirect_uri": self.redirect_uri,
            "response_type": "code",
            "scope": " ".join(scopes),
            "state": state,
            "access_type": "offline",  # Request a refresh token
            "prompt": "consent",  # Ensure consent screen is shown for refresh token
        }
        if code_challenge:
            params["code_challenge"] = code_challenge
            params["code_challenge_method"] = "S256"

        return f"{self.GOOGLE_OAUTH_AUTH_URL}?{urlencode(params)}"

    def exchange_authorization_code(self, code: str, code_verifier: Optional[str] = None) -> Dict[str, Any]:
        data = {
            "client_id": self.client_id,
            "client_secret": self.client_secret,
            "code": code,
            "redirect_uri": self.redirect_uri,
            "grant_type": "authorization_code",
        }
        if code_verifier:
            data["code_verifier"] = code_verifier

        response = requests.post(self.GOOGLE_OAUTH_TOKEN_URL, data=data)
        response.raise_for_status()
        return response.json()

    def get_user_info(self, access_token: str) -> Dict[str, Any]:
        headers = {"Authorization": f"Bearer {access_token}"}
        response = requests.get(self.GOOGLE_USERINFO_URL, headers=headers)
        response.raise_for_status()
        return response.json()


def generate_pkce_challenge() -> Dict[str, str]:
    code_verifier = base64.urlsafe_b64encode(os.urandom(32)).rstrip(b'=').decode('utf-8')
    hashed = hashlib.sha256(code_verifier.encode('utf-8')).digest()
    code_challenge = base64.urlsafe_b64encode(hashed).rstrip(b'=').decode('utf-8')
    return {
        "code_verifier": code_verifier,
        "code_challenge": code_challenge,
        "code_challenge_method": "S256",
    }
