import os
from typing import Dict, Optional
from urllib.parse import urlencode

import httpx

from identity_models import LoginRequest, TokenResponse


class IdentityClient:
    def __init__(self) -> None:
        self.tenant_id = os.environ.get("MICROSOFT_TENANT_ID", "common")
        self.client_id = os.environ.get("MICROSOFT_CLIENT_ID", "")
        self.client_secret = os.environ.get("MICROSOFT_CLIENT_SECRET", "")
        self.authority = f"https://login.microsoftonline.com/{self.tenant_id}/oauth2/v2.0"
        self.graph_base = "https://graph.microsoft.com/v1.0"

    def build_authorization_url(self, request: LoginRequest) -> str:
        params = {
            "client_id": self.client_id,
            "response_type": "code",
            "redirect_uri": request.redirect_uri,
            "response_mode": "query",
            "scope": " ".join(request.scope),
            "state": request.state,
            "nonce": request.nonce,
        }
        if request.code_challenge:
            params["code_challenge"] = request.code_challenge
        if request.code_challenge_method:
            params["code_challenge_method"] = request.code_challenge_method
        return f"{self.authority}/authorize?{urlencode(params)}"

    def exchange_code(self, code: str, redirect_uri: str, code_verifier: Optional[str] = None) -> TokenResponse:
        data: Dict[str, str] = {
            "client_id": self.client_id,
            "client_secret": self.client_secret,
            "grant_type": "authorization_code",
            "code": code,
            "redirect_uri": redirect_uri,
            "scope": "openid profile email offline_access",
        }
        if code_verifier:
            data["code_verifier"] = code_verifier
        response = httpx.post(f"{self.authority}/token", data=data, timeout=30)
        response.raise_for_status()
        payload = response.json()
        return TokenResponse(
            access_token=payload["access_token"],
            token_type=payload.get("token_type", "Bearer"),
            expires_in=payload.get("expires_in"),
            id_token=payload.get("id_token"),
            refresh_token=payload.get("refresh_token"),
            raw=payload,
        )

    def fetch_profile(self, access_token: str) -> Dict[str, object]:
        response = httpx.get(
            f"{self.graph_base}/me",
            headers={"Authorization": f"Bearer {access_token}"},
            timeout=30,
        )
        response.raise_for_status()
        return response.json()
