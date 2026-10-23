import os
import requests
import urllib.parse
import hashlib
import base64
import secrets
from typing import Optional, Dict, Tuple

from identity_models import OAuthConfig, TokenResponse, UserProfile


class IdentityClient:
    def __init__(self):
        self.config = OAuthConfig(
            domain=os.getenv("AUTH0_DOMAIN"),
            client_id=os.getenv("AUTH0_CLIENT_ID"),
            client_secret=os.getenv("AUTH0_CLIENT_SECRET"),
            redirect_uri=os.getenv(
                "AUTH0_REDIRECT_URI", "http://localhost:3000/callback"
            ),
        )
        self.session = requests.Session()
        self.session.headers.update({"User-Agent": "FederatedLogin/1.0"})

    def build_auth_url(
        self,
        state: Optional[str] = None,
        scopes: list[str] = None,
        extra_params: Optional[Dict[str, str]] = None,
    ) -> str:
        if scopes is None:
            scopes = ["openid", "profile", "email"]
        if state is None:
            state = secrets.token_urlsafe(32)
        params = {
            "client_id": self.config.client_id,
            "redirect_uri": self.config.redirect_uri,
            "scope": " ".join(scopes),
            "response_type": "code",
            "state": state,
        }
        if extra_params:
            params.update(extra_params)
        query = urllib.parse.urlencode(params)
        return f"https://{self.config.domain}/authorize?{query}"

    def exchange_code(self, code: str, verifier: Optional[str] = None) -> TokenResponse:
        token_url = f"https://{self.config.domain}/oauth/token"
        data = {
            "grant_type": "authorization_code",
            "client_id": self.config.client_id,
            "code": code,
            "redirect_uri": self.config.redirect_uri,
        }
        if self.config.client_secret:
            data["client_secret"] = self.config.client_secret
        if verifier:
            data["code_verifier"] = verifier
        resp = self.session.post(token_url, data=data)
        resp.raise_for_status()
        tokens = resp.json()
        return TokenResponse(**tokens)

    def get_user_profile(self, access_token: str) -> UserProfile:
        userinfo_url = f"https://{self.config.domain}/userinfo"
        headers = {"Authorization": f"Bearer {access_token}"}
        resp = self.session.get(userinfo_url, headers=headers)
        resp.raise_for_status()
        profile_data = resp.json()
        return UserProfile(
            sub=profile_data["sub"],
            email=profile_data.get("email"),
            name=profile_data.get("name"),
            picture=profile_data.get("picture"),
        )

    @staticmethod
    def generate_pkce_pair() -> Tuple[str, str]:
        verifier = base64.urlsafe_b64encode(os.urandom(32)).decode("ascii").rstrip("=")
        challenge_hash = hashlib.sha256(verifier.encode("ascii")).digest()
        challenge = base64.urlsafe_b64encode(challenge_hash).decode("ascii").rstrip("=")
        return verifier, challenge
