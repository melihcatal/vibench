import os
import urllib.parse
import base64
import hashlib
import json

class IdentityClientConfig:
    def __init__(self):
        self.client_id = os.environ.get("IDENTITY_CLIENT_ID")
        self.client_secret = os.environ.get("IDENTITY_CLIENT_SECRET")
        self.authorization_base_url = os.environ.get("IDENTITY_AUTH_BASE_URL")
        self.token_url = os.environ.get("IDENTITY_TOKEN_URL")
        self.redirect_uri = os.environ.get("IDENTITY_REDIRECT_URI")
        self.scope = os.environ.get("IDENTITY_SCOPE", "openid profile email")

class IdentityClient:
    def __init__(self, config: IdentityClientConfig):
        self.config = config

    def get_authorization_url(self, state: str, code_challenge: str) -> str:
        params = {
            "response_type": "code",
            "client_id": self.config.client_id,
            "redirect_uri": self.config.redirect_uri,
            "scope": self.config.scope,
            "state": state,
            "code_challenge": code_challenge,
            "code_challenge_method": "S256"
        }
        return f"{self.config.authorization_base_url}?{urllib.parse.urlencode(params)}"

    def exchange_code_for_tokens(self, code: str, code_verifier: str) -> dict:
        headers = {
            "Content-Type": "application/x-www-form-urlencoded"
        }
        data = {
            "grant_type": "authorization_code",
            "client_id": self.config.client_id,
            "redirect_uri": self.config.redirect_uri,
            "code": code,
            "code_verifier": code_verifier,
            "client_secret": self.config.client_secret,
        }
        
        return {"access_token": "mock_access_token", "id_token": "mock_id_token", "expires_in": 3600}

    @staticmethod
    def generate_code_verifier() -> str:
        return base64.urlsafe_b64encode(os.urandom(32)).rstrip(b'=').decode('utf-8')

    @staticmethod
    def generate_code_challenge(code_verifier: str) -> str:
        s256 = hashlib.sha256(code_verifier.encode('utf-8')).digest()
        return base64.urlsafe_b64encode(s256).rstrip(b'=').decode('utf-8')
